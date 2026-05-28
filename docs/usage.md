# Usage

This page covers installation, CLI usage, TOML profiles, and Python API
examples for CHAMANP.

## Installation

```bash
pip install chamanp
```

CHAMANP requires Python 3.11 or 3.12 and depends on
[RDKit](https://www.rdkit.org/), pandas, and numpy.

The command above installs the Python package and CLI. It does not install the
repository-only example files used below, such as `examples/example_chamanp.csv`
or `source_data/coconut_taxonomy.json`.

## Quick Start

The fastest way to try CHAMANP with the included example is from a source
checkout of the repository:

```bash
git clone https://github.com/NanoBiostructuresRG/chamanp.git
cd chamanp
python -m pip install -e .
```

The example uses:

- `examples/example_chamanp.csv`, a small COCONUT-like molecular table.
- `source_data/coconut_taxonomy.json`, a collection taxonomy for the reference
  COCONUT workflow.

Create `example-chamanp.toml` in the repository root:

```toml
database_path = "examples/example_chamanp.csv"
reports_path = "artifacts/reports"
collection_taxonomy_path = "source_data/coconut_taxonomy.json"
target_collections = ["ChEMBL NPs"]
collection_tag = "chembl_example"
collection_logic = "OR"
morgan_radius = 2
morgan_bits = 1024
selected_properties = [
  "identifier",
  "canonical_smiles",
  "name",
  "molecular_weight",
  "alogp",
  "topological_polar_surface_area",
  "np_likeness",
  "collections",
]
remove_stereo_duplicates = true
```

Validate the profile:

```bash
chamanp check-config example-chamanp.toml
```

Expected output:

```text
Configuration OK: example-chamanp.toml
```

Run the preparation workflow:

```bash
chamanp run example-chamanp.toml
```

Expected CLI output:

```text
CHAMANP run completed.
Status: completed
Output directory: artifacts
```

For this example dataset, the report records 15 input rows, 15 retained
compounds for `ChEMBL NPs`, 0 invalid SMILES rows, and 15 fingerprinted
molecules.

For most users, start with these essential outputs:

```text
artifacts/filtered_chembl_example.csv
artifacts/valid_metadata_chembl_example.csv
artifacts/X_chembl_example.npy
artifacts/reports/report_dbprep_chembl_example.txt
```

Use these audit outputs when you need to inspect intermediate processing:

```text
artifacts/curated_chembl_example.csv
artifacts/invalid_smiles_chembl_example.csv
```

In this small example, some CSV files may look identical because all rows match
`ChEMBL NPs` and all SMILES can be fingerprinted. In larger datasets, the
curated, filtered, valid-metadata, and invalid-SMILES files usually diverge as
deduplication, collection filtering, and fingerprint validation occur.

If you installed CHAMANP from PyPI and are not working from a source checkout,
use the same TOML structure with your own local CSV and taxonomy JSON paths.

## How to Write the TOML Profile

A TOML profile is not generated from the CSV. It is a small configuration file
that you write after inspecting your CSV and deciding what subset CHAMANP
should prepare.

The CSV provides the molecular data. The TOML profile tells CHAMANP how to use
that data:

| TOML field | How to choose it from your data |
|------------|---------------------------------|
| `database_path` | Path to your input CSV file. |
| `collection_taxonomy_path` | Path to the JSON file that lists valid collection names. |
| `target_collections` | Collection label or labels to extract from the CSV `collections` column. These names must exist in the taxonomy JSON. |
| `collection_logic` | Use `OR` to keep molecules present in any requested collection, or `AND` to keep only molecules present in all requested collections. |
| `selected_properties` | Column names from the CSV that should be retained in the output tables. |
| `reports_path` | Folder where the text report should be written. |
| `collection_tag` | Short file-safe tag used in output filenames. |
| `morgan_radius` and `morgan_bits` | RDKit Morgan fingerprint settings. |
| `remove_stereo_duplicates` | Whether CHAMANP should collapse stereochemistry-related duplicate structures during curation. |

For the included example CSV, the header starts with:

```text
identifier,canonical_smiles,name,molecular_weight,alogp,topological_polar_surface_area,np_likeness,collections
```

Because `canonical_smiles` and `collections` are present, CHAMANP can curate
molecules and filter by collection. Because the file contains labels such as
`ChEMBL NPs`, the example TOML can request:

```toml
database_path = "examples/example_chamanp.csv"
collection_taxonomy_path = "source_data/coconut_taxonomy.json"
target_collections = ["ChEMBL NPs"]
collection_logic = "OR"
```

For your own CSV, create a TOML profile by changing the paths, collection
names, retained columns, and output tag to match your dataset.

## Python API Examples

=== "ChamanpConfig"

    ```python
    from chamanp import ChamanpConfig

    cfg = ChamanpConfig(
        DATABASE_PATH="examples/example_chamanp.csv",
        REPORTS_PATH="artifacts/reports",
        COLLECTION_TAXONOMY_PATH="source_data/coconut_taxonomy.json",
        TARGET_COLLECTIONS=["ChEMBL NPs"],
        COLLECTION_TAG="chembl",
        COLLECTION_LOGIC="OR",
        MORGAN_RADIUS=2,
        MORGAN_BITS=1024,
        SELECTED_PROPERTIES=[
            "identifier",
            "canonical_smiles",
            "name",
            "molecular_weight",
            "alogp",
            "topological_polar_surface_area",
            "np_likeness",
            "collections",
        ],
        REMOVE_STEREO_DUPLICATES=True,
    )
    ```

=== "validate_config"

    ```python
    from chamanp import ChamanpConfig, validate_config

    cfg = ChamanpConfig.from_toml("my-chamanp-profile.toml")
    validate_config(cfg)
    ```

=== "run"

    ```python
    from chamanp import ChamanpConfig, run

    cfg = ChamanpConfig.from_toml("my-chamanp-profile.toml")
    result = run(cfg)
    print(result.valid_molecules_count)
    print(result.fingerprints_path)
    ```

=== "ChamanpResult"

    ```python
    from chamanp import ChamanpConfig, ChamanpResult, run

    cfg = ChamanpConfig.from_toml("my-chamanp-profile.toml")
    result = run(cfg)

    assert isinstance(result, ChamanpResult)
    print(result.status)
    print(result.report_path)
    ```

## Public API

| Symbol | Description |
|--------|-------------|
| <a href="../api/"><code>ChamanpConfig</code></a> | Runtime configuration object |
| <a href="../api/"><code>ChamanpResult</code></a> | Lightweight result returned by `run()` |
| <a href="../api/"><code>validate_config</code></a> | Validate configuration before execution |
| <a href="../api/"><code>run</code></a> | Execute the CHAMANP pipeline |
| `__version__` | Package version string |

See the <a href="../api/">API Reference</a> for public API documentation
generated from the package docstrings.
