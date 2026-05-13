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

The development environment used for the `dev-v1.0.1` baseline is:

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

The current baseline contains 21 tests covering isolated components:

- `path_manager`
- `collection_utils`
- `filter`
- `curator`
- `fingerprints`

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
|   `-- reporter.py                   # Technical report generation
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

To ignore stereochemistry in SMILES during deduplication:

```python
REMOVE_STEREO_DUPLICATES = True
```

To filter compounds by COCONUT collection:

```python
TARGET_COLLECTIONS = ["PubChem NPs"]
COLLECTION_TAG = "pubchem"
COLLECTION_LOGIC = "OR"
```

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
- `X_*.npy`
- `reports/report_dbprep_*.txt`
- `pipeline.log`

## Development Status

CHAMANP is currently in pre-stable development. The `dev-v1.0.1` work is intended to establish a conservative documentation and dependency baseline before future functional changes.

## Future Extensions

- Integration with bioactivity repositories such as ChEMBL or PubChem BioAssay.
- Support for additional fingerprint types and molecular descriptors.
- Broader test coverage and reproducibility metadata.
- Future integration into the LigandHub suite.

## Author

Developed by Flavio F. Contreras-Torres, Tecnologico de Monterrey.

## License

This project is licensed under the terms of the [MIT License](LICENSE). See the LICENSE file for details.
