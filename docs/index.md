# CHAMANP

<section class="cp-hero">
  <div class="cp-hero__content">
    <p class="cp-eyebrow">Natural products curation</p>
    <div class="cp-brand" aria-label="CHAMANP">
      <img class="cp-brand__logo" src="assets/images/logo-cafe.svg" alt="CHAMANP logo">
      <span class="cp-wordmark">CHAMANP</span>
    </div>
    <p class="cp-subtitle">
      Prepare collection-aware natural-product datasets from raw molecular tables.
    </p>
    <div class="cp-actions">
      <a class="md-button md-button--primary" href="#installation">Install</a>
      <a class="md-button" href="#quick-start">Quick start</a>
      <a class="md-button" href="api/">API Reference</a>
    </div>
    <div class="cp-badges" aria-label="Project badges">
      <img alt="CI" src="https://github.com/NanoBiostructuresRG/chamanp/actions/workflows/ci.yml/badge.svg">
      <img alt="PyPI" src="https://img.shields.io/pypi/v/chamanp">
      <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/chamanp">
      <img alt="License: LGPL v3+" src="https://img.shields.io/badge/License-LGPL_v3%2B-blue.svg">
    </div>
  </div>
</section>

!!! note "Pre-stable"
    CHAMANP is currently in Alpha-stage development. The public API is being
    hardened before stability is declared.

## Installation

```bash
pip install chamanp
```

CHAMANP requires Python 3.11 or 3.12 and depends on
[RDKit](https://www.rdkit.org/), pandas, and numpy.

The command above installs the Python package and CLI. It does not install the
repository-only example files used below, such as `examples/example_chamanp.csv`
or `source_data/coconut_taxonomy.json`.

<section class="cp-panel">
  <div class="cp-grid cp-grid--three">
    <article class="cp-card">
      <span class="cp-card__icon">01</span>
      <h3>Validate first</h3>
      <p>Check paths, collection names, tags, and fingerprint settings before molecular processing begins.</p>
    </article>
    <article class="cp-card">
      <span class="cp-card__icon">02</span>
      <h3>Separate collections</h3>
      <p>Partition compounds assigned to one or several source collections using exact collection labels.</p>
    </article>
    <article class="cp-card">
      <span class="cp-card__icon">03</span>
      <h3>Export fingerprints</h3>
      <p>Write RDKit Morgan fingerprints with metadata and run reports that record generated paths and counts.</p>
    </article>
  </div>
</section>

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

## Why CHAMANP?

Public natural-product databases are commonly distributed as tabular molecular
records in which compounds, structures, identifiers, and collection labels are
stored together. In practice, one compound may be associated with a single
collection or with several collections at the same time. This creates a
practical problem for downstream analysis: the researcher must decide whether
the working unit is the compound itself, the collection to which it belongs, or
the relationship between both.

This distinction matters when the objective is to study collections rather than
only individual compounds. For example, a researcher may want to analyze the
chemical space of a fungal, marine, plant, bacterial, or food-derived
collection. To do that reproducibly, the original table has to be partitioned
according to collection labels while keeping track of duplicated structures,
invalid SMILES, and compounds shared across collections.

**CHAMANP** (Curation and Hierarchical Analysis for Molecular Annotation of Natural Products) was created for this preparation step. It takes raw natural-product
molecular tables and produces curated, traceable, collection-aware datasets
that can be used for fingerprint generation and downstream cheminformatics or
machine learning workflows. Current development uses COCONUT as the reference
dataset, but the workflow is intended to remain applicable to other tabular
natural-product sources.

The name intentionally echoes *shaman*. In this context, CHAMANP acts as an
interpreter between a dispersed molecular table and the collection-level
subsets requested by the researcher. Its role is not only to clean molecular
records, but to make explicit which compounds belong to which collections,
including cases where the same compound belongs to more than one collection.

!!! tip "Dataset preparation contract"
    CHAMANP keeps molecular dataset preparation traceable: configuration is
    validated before execution, curated and filtered tables are written as
    artifacts, invalid SMILES are recorded, and RDKit Morgan fingerprints are
    exported with reproducible names.

## Collection Taxonomy

COCONUT records collection membership in a `collections` field. A single
molecule can be associated with several source collections, for example
`ChEMBL NPs|DrugBankNP`. CHAMANP reads those labels exactly and can keep
molecules that match one requested collection (`OR`) or all requested
collections (`AND`).

The `source_data/coconut_taxonomy.json` file defines the valid collection names
used by the reference COCONUT workflow. CHAMANP checks requested
`target_collections` against this taxonomy before processing, so a typo such as
`Chembl NP` fails before any output tables are written. In this workflow, the
database provides compound memberships, the taxonomy defines the allowed
labels, and CHAMANP separates the requested chemical subset.

## What You Provide and Receive

CHAMANP is a preparation step between a raw natural-product table and the files
that a cheminformatics or machine learning workflow can consume. A typical run
has this contract:

| Stage | User provides | CHAMANP does | User receives |
|-------|---------------|--------------|---------------|
| Input | A CSV table with `canonical_smiles`, `collections`, and selected metadata columns. | Reads the table and keeps the configured properties. | A starting table for the run. |
| Taxonomy | A collection taxonomy JSON file such as `source_data/coconut_taxonomy.json`. | Uses it as the allowed list for requested collection names. | An early error if a requested collection is not in the taxonomy. |
| Configuration | A `ChamanpConfig` object or TOML profile with paths, target collections, fingerprint settings, and output location. | Validates required paths, collection names, tags, and Morgan fingerprint parameters before processing. | Explicit configuration errors before chemical processing begins. |
| Curation | Raw molecular rows that may contain duplicates, invalid SMILES, or multiple collection memberships. | Curates SMILES with RDKit, handles duplicates, separates molecules by exact collection labels, and records invalid molecules. | Curated and collection-filtered CSV artifacts. |
| Fingerprints | Valid molecules after curation and collection filtering. | Generates RDKit Morgan fingerprints using the configured radius and bit length. | `X_*.npy` fingerprint matrix plus aligned valid-molecule metadata. |
| Report | The completed run context. | Writes a preparation report with version, configuration, counts, and artifact paths. | A text report and a `ChamanpResult` object pointing to generated files. |

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
| <a href="api/"><code>ChamanpConfig</code></a> | Runtime configuration object |
| <a href="api/"><code>ChamanpResult</code></a> | Lightweight result returned by `run()` |
| <a href="api/"><code>validate_config</code></a> | Validate configuration before execution |
| <a href="api/"><code>run</code></a> | Execute the CHAMANP pipeline |
| `__version__` | Package version string |

See the <a href="api/">API Reference</a> for public API documentation generated
from the package docstrings.

## Citation

```text
Contreras-Torres, F. F. (2026). CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products (v0.19.0). Zenodo. https://doi.org/10.5281/zenodo.20249166
```

Use `CITATION.cff` as the authoritative machine-readable citation metadata for
CHAMANP. Citation metadata is updated with each release.

## License

This project is licensed under the terms of the
[GNU Lesser General Public License v3.0 or later](https://github.com/NanoBiostructuresRG/chamanp/blob/main/LICENSE).
SPDX identifier: `LGPL-3.0-or-later`.
