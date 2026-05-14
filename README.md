# CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products

[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL_v3%2B-blue.svg)](LICENSE)

CHAMANP is a Python library for systematic, reproducible curation and preparation of molecular datasets of natural products.

CHAMANP fills a gap between raw molecular databases and analysis-ready datasets for cheminformatics or machine learning pipelines. Current development uses COCONUT as the reference dataset.

It helps turn raw molecular tables into curated, traceable, fingerprint-ready datasets for reproducible cheminformatics workflows.

CHAMANP is pre-stable. The repository workflow is the current complete execution path, while the package API is being introduced gradually.

## Why CHAMANP?

Researchers often prepare molecular datasets with ad hoc scripts that are difficult to validate, repeat, or share. CHAMANP provides a more reproducible preparation workflow with:

- Early configuration validation before chemical processing begins.
- Collection-based filtering for natural product subsets.
- RDKit Morgan fingerprint generation.
- Invalid SMILES traceability.
- Consistent output artifacts and preparation reports.
- Better reproducibility across runs, collaborators, and downstream analyses.

## Who Should Use It?

CHAMANP is intended for:

- Natural products researchers preparing compound datasets.
- Cheminformatics researchers building analysis-ready molecular tables.
- Researchers preparing molecular datasets for machine learning.
- Drug discovery, repositioning, nutrition, biomedicine, and nutraceutics groups.
- Developers building applications that need reproducible molecular dataset preparation.

CHAMANP is intended to remain independent and reusable. LigandHub is a future consumer, not a dependency or coupling target.

## What CHAMANP Does Today

The current repository pipeline can:

- Read tabular molecular datasets with SMILES and metadata.
- Validate and curate SMILES with RDKit.
- Handle duplicates and optional stereochemistry-related duplicate removal.
- Filter molecules by configured collection labels.
- Validate collection and execution configuration before running.
- Generate RDKit Morgan fingerprints.
- Record invalid SMILES encountered during fingerprint generation.
- Write curated datasets, filtered datasets, fingerprint matrices, valid metadata, invalid SMILES files, and preparation reports.

CHAMANP does not currently provide molecular property prediction, docking, virtual screening, or a stable public execution API.

## COCONUT As Reference Dataset

COCONUT is the current reference dataset used during CHAMANP development. It demonstrates and validates the current engine because it provides natural product molecules, SMILES strings, and collection metadata.

CHAMANP is not intended to be COCONUT-specific. It is designed to evolve toward natural product molecular databases that can be represented as tabular files with SMILES and collection metadata.

The current COCONUT taxonomy file is a project artifact for the reference workflow, not the general definition of CHAMANP. Future work should make clear which assumptions are COCONUT-specific and which are universal across supported datasets.

## Current Usable Modes

### Repository Pipeline Workflow

The complete execution workflow is currently repository-based:

1. Prepare the required source data.
2. Edit `config.py`.
3. Run the pipeline from the repository root:

```bash
python main.py
```

This executes:

```text
input curation -> collection validation -> filtering -> fingerprinting -> reporting
```

### Minimal Package API

CHAMANP also has a minimal importable package doorway:

```python
import chamanp
from chamanp import __version__, ChamanpConfig
```

`ChamanpConfig` is the first public runtime configuration object. It provides an importable configuration contract for future reusable workflows and does not change the current repository-based pipeline behavior.

The full execution API is not public yet.

## Current Public API

Current public imports:

```python
import chamanp
from chamanp import __version__, ChamanpConfig
```

These are not current public `chamanp` exports:

- `Pipeline`
- `validate_config`
- CLI commands
- YAML/TOML/JSON configuration profiles

Future releases may expose a public execution API, but that API is still a draft direction.

## Minimal Usage Examples

### Run The Current Repository Pipeline

```bash
python main.py
```

### Create A Configuration Object

```python
from chamanp import ChamanpConfig

cfg = ChamanpConfig(
    DATABASE_PATH="source_data/coconut_05-2025.csv",
    REPORTS_PATH="artifacts/reports",
    COLLECTION_TAXONOMY_PATH="source_data/coconut_taxonomy.json",
    TARGET_COLLECTIONS=["PubChem NPs"],
    COLLECTION_TAG="pubchem",
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

### Build A Configuration From A Module

```python
from chamanp import ChamanpConfig
import my_config

cfg = ChamanpConfig.from_module(my_config)
```

This creates a configuration object from a module with the expected uppercase configuration attributes. It does not run the pipeline.

## Installation Status

CHAMANP is currently pre-stable.

The package foundation exists, and the minimal public package imports are available. Because `core/` and `utils/` have not yet been migrated into `chamanp/`, CHAMANP is not yet a fully packaged execution library. The repository workflow remains the current complete execution path.

CHAMANP currently targets Python 3.11. Because CHAMANP uses RDKit, conda/mamba is the recommended environment path:

```bash
mamba env create -f environment.yml
mamba activate chamanp_env
```

or:

```bash
conda env create -f environment.yml
conda activate chamanp_env
```

Alternatively, install runtime dependencies with pip:

```bash
pip install -r requirements.txt
```

For development and testing tools with pip:

```bash
pip install -r requirements-dev.txt
```

## Inputs

The current repository workflow expects:

- A molecular table with SMILES and metadata.
- A collection taxonomy JSON file.
- Configuration values in `config.py`.

Large/raw datasets are not tracked in this repository. To run the current reference workflow, provide the COCONUT source CSV at:

```text
source_data/coconut_05-2025.csv
```

The expected source fields are configured in `config.py`:

```python
SELECTED_PROPERTIES = [
    "identifier",
    "canonical_smiles",
    "name",
    "molecular_weight",
    "alogp",
    "topological_polar_surface_area",
    "np_likeness",
    "collections",
]
```

## Configuration

Pipeline behavior is currently controlled by the repository-level `config.py`.

Before the pipeline runs, CHAMANP validates the active configuration and fails early with a `ConfigurationError` if required inputs or execution parameters are invalid. The preflight check verifies that:

- The configured database CSV exists.
- The configured collection taxonomy path exists.
- `TARGET_COLLECTIONS` is a non-empty collection of non-empty strings.
- A plain string is not accepted as `TARGET_COLLECTIONS`.
- `COLLECTION_LOGIC` is `OR` or `AND`.
- `COLLECTION_TAG` is safe for artifact filenames.
- Morgan fingerprint parameters are valid integers.

Example collection and fingerprint settings:

```python
TARGET_COLLECTIONS = ["PubChem NPs"]
COLLECTION_TAG = "pubchem"
COLLECTION_LOGIC = "OR"
MORGAN_RADIUS = 2
MORGAN_BITS = 1024
```

To ignore stereochemistry in SMILES during deduplication:

```python
REMOVE_STEREO_DUPLICATES = True
```

Collection filtering uses exact collection-label matching. Multiple collection labels in the `collections` field are expected to be separated by semicolons, and surrounding whitespace around each label is stripped before matching. Matching is case-sensitive, which avoids substring false positives: for example, `PubChem NPs` does not match `NotPubChem NPs`.

## Outputs

Generated files are written under `artifacts/`, including:

- `curated_*.csv`
- `filtered_*.csv`
- `valid_metadata_*.csv`
- `invalid_smiles_*.csv`
- `X_*.npy`
- `reports/report_dbprep_*.txt`
- `pipeline.log`

At a high level, CHAMANP produces:

- A curated dataset.
- A filtered dataset.
- A Morgan fingerprint matrix.
- Valid molecule metadata.
- Invalid SMILES traceability.
- A preparation report with version, configuration, and count metadata.

`invalid_smiles_{tag}.csv` records rows whose configured SMILES column cannot be parsed by RDKit during fingerprint generation. This artifact improves traceability and does not change the valid fingerprint matrix or valid metadata outputs.

## Testing

Run the baseline test suite with:

```bash
python -m pytest tests
```

The current baseline contains focused tests covering isolated components:

- `path_manager`
- `collection_utils`
- `filter`
- `curator`
- `fingerprints`
- `preflight`
- `reporter`
- `result_manager`
- `main`
- `package imports`
- `ChamanpConfig`

These tests do not run the full pipeline and do not require the full COCONUT source CSV.

On Windows, if pytest cannot access the default temporary directory, use a local pytest temporary directory. For example, in the currently validated local environment:

```powershell
New-Item -ItemType Directory -Force .pytest_tmp | Out-Null
C:\Users\Usuario\.conda\envs\chamanp_env\python.exe -m pytest tests -p no:cacheprovider --basetemp .pytest_tmp
Remove-Item -Recurse -Force .pytest_tmp
```

## Project Structure

```text
CHAMANP/
|-- main.py                           # Repository entry point
|-- config.py                         # Repository pipeline configuration
|-- README.md                         # Project overview and usage guide
|-- DESIGN.md                         # Internal strategic design reference
|-- LICENSE                           # Project license notice
|-- COPYING                           # GNU GPLv3 text
|-- COPYING.LESSER                    # GNU LGPLv3 text
|-- CITATION.cff                      # Citation metadata
|-- requirements.txt                  # Runtime dependencies
|-- requirements-dev.txt              # Development/test dependencies
|-- environment.yml                   # Conda/mamba environment
|-- pyproject.toml                    # Package metadata
|-- CHANGELOG.md                      # Development history
|-- chamanp/                          # Minimal package namespace
|   |-- __init__.py                   # Public package doorway
|   |-- config.py                     # Public configuration object
|   `-- version.py                    # Package version source
|-- core/                             # Internal pipeline modules
|   |-- base_pipeline.py              # Pipeline orchestrator
|   |-- curator.py                    # Input curation and validation
|   |-- filter.py                     # Property and collection-based filtering
|   |-- fingerprints.py               # Molecular fingerprint generation
|   |-- preflight.py                  # Configuration validation before execution
|   |-- reporter.py                   # Technical report generation
|   `-- version.py                    # Backward-compatible version bridge
|-- utils/                            # Internal auxiliary utilities
|   |-- path_manager.py               # Centralized artifact paths
|   |-- result_manager.py             # Report header and file writing
|   `-- collection_utils.py           # Collection taxonomy validation
|-- source_data/
|   |-- README.md                     # Source-data policy
|   |-- coconut_05-2025.csv           # User-provided source database file
|   `-- coconut_taxonomy.json         # Tracked taxonomy reference
`-- artifacts/                        # Generated output files
    `-- reports/                      # Execution reports
```

`core/` and `utils/` are internal today. They should not be treated as stable public API.

## Development Status

CHAMANP is still in pre-stable development.

- `v0.1.0` established the corrected pre-stable baseline.
- `v0.2.0` focused on centralized project metadata and reproducible report execution metadata.
- `v0.3.0` focused on configuration validation and execution preflight.
- `v0.4.0` established the package foundation and public API doorway.
- `v0.5.0` introduced `ChamanpConfig` as the first public runtime configuration object.
- `v0.6.0` focuses on external-facing documentation and the public usability contract.

The earlier `dev-v1.0.1` work established the documentation, dependency, and testing baseline that was incorporated into `v0.1.0`. The development environment used for that baseline was:

```text
Python 3.11
pandas 3.0.3
numpy 2.4.3
scipy 1.15.3
rdkit 2025.09.2
pytest 8.3.4
```

## Future Direction

Planned development remains conservative:

- Keep `import chamanp` side-effect free.
- Keep CHAMANP independent from LigandHub while remaining easy for LigandHub to consume.
- Migrate internal modules into private package paths before exposing a public execution API.
- Add a public execution API only after import-time side effects are resolved.
- Defer CLI commands and YAML/TOML/JSON configuration profiles until the public Python API is clearer.

Future extension areas may include:

- Integration with bioactivity repositories such as ChEMBL or PubChem BioAssay.
- Support for additional fingerprint types and molecular descriptors.
- Broader test coverage and reproducibility metadata.
- Future integration into the LigandHub suite as one consumer of CHAMANP.

## Author

Developed by Flavio F. Contreras-Torres, Tecnologico de Monterrey.

## License

This project is licensed under the terms of the [GNU Lesser General Public License v3.0 or later](LICENSE). SPDX identifier: `LGPL-3.0-or-later`.
