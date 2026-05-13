# CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

CHAMANP is a pre-stable development prototype for the curated preparation of molecular datasets used in cheminformatics workflows. It is being prepared as a future component of the LigandHub suite.

The primary objective of CHAMANP is to support systematic and reproducible preparation of curated molecular datasets for molecular annotation, natural products research, and downstream machine learning workflows.

## Current Scope

The current pipeline supports:

- Standardized curation and deduplication of chemical structures.
- Collection-based filtering of compounds using COCONUT collection metadata.
- Generation of Morgan molecular fingerprints with RDKit.
- Report-driven documentation of dataset preparation runs.

This repository is under active development and should not yet be treated as a stable production release.

## Python Target

CHAMANP currently targets Python 3.11.

The earlier `dev-v1.0.1` work established the documentation, dependency, and testing baseline that was incorporated into `v0.1.0`. The development environment used for that baseline is:

```text
Python 3.11
pandas 3.0.3
numpy 2.4.3
scipy 1.15.3
rdkit 2025.09.2
pytest 8.3.4
```

## Installation

Because CHAMANP uses RDKit, the recommended installation path is conda/mamba:

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
|-- main.py                           # Entry point
|-- config.py                         # Global pipeline configuration
|-- README.md                         # Project overview and usage guide
|-- LICENSE                           # MIT license
|-- CITATION.cff                      # Citation metadata
|-- requirements.txt                  # Runtime dependencies
|-- requirements-dev.txt              # Development/test dependencies
|-- environment.yml                   # Conda/mamba environment
|-- CHANGELOG.md                      # Development history
|-- core/                             # Pipeline modules
|   |-- base_pipeline.py              # Pipeline orchestrator
|   |-- curator.py                    # Input curation and validation
|   |-- filter.py                     # Property and collection-based filtering
|   |-- fingerprints.py               # Molecular fingerprint generation
|   |-- preflight.py                  # Configuration validation before execution
|   |-- reporter.py                   # Technical report generation
|   `-- version.py                    # Centralized project metadata
|-- utils/                            # Auxiliary utilities
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

## Source Data

Large/raw datasets are not tracked in this repository. To run the current pipeline, provide the COCONUT source CSV at:

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
    "collections"
]
```

## Configuration

Pipeline behavior is currently controlled in `config.py`.

Before the pipeline runs, CHAMANP validates the active configuration and fails early with a `ConfigurationError` if required inputs or execution parameters are invalid. The preflight check verifies that the configured database CSV and collection taxonomy paths exist, target collections are not empty, collection logic is `OR` or `AND`, the collection tag is safe for artifact filenames, and Morgan fingerprint parameters are valid integers.

To ignore stereochemistry in SMILES during deduplication:

```python
REMOVE_STEREO_DUPLICATES = True
```

To filter compounds by COCONUT collection:

```python
TARGET_COLLECTIONS = ["PubChem NPs"]
COLLECTION_TAG = "pubchem"
COLLECTION_LOGIC = "OR"
MORGAN_RADIUS = 2
MORGAN_BITS = 1024
```

Collection filtering uses exact collection-label matching. Multiple collection labels in the `collections` field are expected to be separated by semicolons, and surrounding whitespace around each label is stripped before matching. Matching is case-sensitive, which avoids substring false positives: for example, `PubChem NPs` does not match `NotPubChem NPs`.

## How to Run

From the project root directory:

```bash
python main.py
```

This executes the current pipeline:

```text
input curation -> collection validation -> filtering -> fingerprinting -> reporting
```

## Output

Generated files are written under `artifacts/`, including:

- `curated_*.csv`
- `filtered_*.csv`
- `valid_metadata_*.csv`
- `invalid_smiles_*.csv`
- `X_*.npy`
- `reports/report_dbprep_*.txt`
- `pipeline.log`

`invalid_smiles_{tag}.csv` records rows whose configured SMILES column cannot be parsed by RDKit during fingerprint generation. This artifact improves traceability and does not change the valid fingerprint matrix or valid metadata outputs.

Future generated reports include the invalid SMILES row count and the `invalid_smiles_{tag}.csv` path when invalid SMILES traceability is available from the pipeline. The tracked historical report under `artifacts/reports/` was not regenerated as part of this development change.

Future reports identify the project using centralized metadata from `core/version.py`, including the CHAMANP development version, execution date, and pre-stable status.

Future reports also include execution metadata already available to the pipeline: input CSV path, collection tag, fingerprint radius, fingerprint bit length, total molecule counts, valid fingerprinted molecules, and invalid SMILES counts.

## Development Status

CHAMANP is still in pre-stable development. Version `v0.1.0` established the corrected pre-stable baseline, including conservative documentation, dependency declarations, isolated tests, exact collection-label matching, invalid SMILES traceability, and report traceability for invalid SMILES. Version `v0.2.0` focused on centralized project metadata and reproducible report execution metadata. The `dev-v0.3.0` work focuses on configuration validation and execution preflight without changing the chemical curation, filtering, or fingerprinting logic.

## Future Extensions

- Integration with bioactivity repositories such as ChEMBL or PubChem BioAssay.
- Support for additional fingerprint types and molecular descriptors.
- Broader test coverage and reproducibility metadata.
- Future integration into the LigandHub suite.

## Author

Developed by Flavio F. Contreras-Torres, Tecnologico de Monterrey.

## License

This project is licensed under the terms of the [MIT License](LICENSE). See the LICENSE file for details.
