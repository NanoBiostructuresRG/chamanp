# CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products

[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL_v3%2B-blue.svg)](LICENSE)

CHAMANP is a Python library for systematic, reproducible curation and preparation of molecular datasets of natural products.

CHAMANP fills a gap between raw molecular databases and analysis-ready datasets for cheminformatics or machine learning pipelines. Current development uses COCONUT as the reference dataset.

It helps turn raw molecular tables into curated, traceable, fingerprint-ready datasets for reproducible cheminformatics workflows.

CHAMANP is pre-stable and is currently being prepared for a future stable,
publishable release. The repository workflow remains available, while the
current public package API is being hardened before stability is declared.

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

CHAMANP does not currently provide molecular property prediction, docking,
virtual screening, or a stable public API. A pre-stable public API is available
through `ChamanpConfig`, `ChamanpResult`, `validate_config`, and `run`.

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

### Package API

CHAMANP also has an importable package doorway:

```python
import chamanp
from chamanp import __version__, ChamanpConfig, ChamanpResult, validate_config, run
```

`ChamanpConfig` is the public runtime configuration object. `validate_config(config)` validates configuration before execution. `run(config)` validates the configuration, executes the current pipeline behavior, writes configured artifacts to disk, and returns a lightweight `ChamanpResult`.

`ChamanpResult` contains artifact paths and summary counts. Successful runs currently use `status="completed"`. It does not load fingerprint matrices, datasets, or reports into memory by default. Execution failures raise exceptions rather than returning a failed `ChamanpResult`.

## Current Public API

Current public imports:

```python
import chamanp
from chamanp import __version__, ChamanpConfig, ChamanpResult, validate_config, run
```

This is the current pre-stable public contract being prepared for a future
stable publication. The eventual stable release number is not fixed here.

These are not current public `chamanp` exports:

- `Pipeline`
- YAML/JSON configuration profiles
- Environment-variable or command-line configuration overrides

`Pipeline` remains private and is not exported from `chamanp`.

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

### Load A TOML Configuration Profile

```python
from chamanp import ChamanpConfig, validate_config, run

cfg = ChamanpConfig.from_toml("examples/chamanp.toml")
validate_config(cfg)
result = run(cfg)
```

TOML loading uses lower_snake_case keys and builds a `ChamanpConfig` object. It does not run the pipeline and does not replace `validate_config(config)`. Unknown TOML fields fail clearly instead of being ignored. The repository-level `config.py` workflow remains supported for local runs.

### Use The Minimal CLI

```bash
chamanp --version
chamanp check-config examples/chamanp.toml
chamanp run examples/chamanp.toml
```

The CLI uses TOML profiles. `check-config` loads and validates a profile without running the pipeline. `run` loads the profile, validates it, executes CHAMANP, and prints a short summary from the returned `ChamanpResult`.

The `examples/chamanp.toml` profile is provided in the repository and source
distribution as a minimal reference profile. Wheels do not currently install
example profiles as package resources. Users installing from a wheel or from a
future PyPI release should create their own TOML profile or copy the reference
profile from the source distribution or repository.

CLI errors are user-facing by default:

```text
Error: <message>
```

Python tracebacks are not shown by default.

### Validate And Run From Python

```python
from chamanp import ChamanpConfig, ChamanpResult, validate_config, run
import my_config

cfg = ChamanpConfig.from_module(my_config)
validate_config(cfg)
result = run(cfg)
assert isinstance(result, ChamanpResult)
print(result.valid_molecules_count)
print(result.fingerprints_path)
```

`run(config)` preserves the current disk-output behavior. It writes configured artifacts and reports to disk, then returns a `ChamanpResult` with paths and summary counts. The result object does not load `X_*.npy`, CSV files, or reports into memory by default.

For successful runs, `result.status` is currently `"completed"`. If validation or execution fails, `run(config)` raises the underlying exception and does not return a failed result object.

## Installation Status

CHAMANP is currently pre-stable.

The package foundation exists, and the public package imports for configuration validation and execution are available. Internal implementation modules live under private package namespaces, `chamanp/_core/` and `chamanp/_utils/`. These private namespaces are not user-facing API. The repository workflow remains available while the Python API continues to mature.

For more detailed installation and distribution notes, see [INSTALL.md](INSTALL.md).

CHAMANP is an independent package. It is not developed specifically for LigandHub, although LigandHub-API may become an early downstream consumer through pip installation in Docker. CHAMANP should remain reusable by scientists, notebooks, pipelines, servers, and external applications.

CHAMANP currently targets Python 3.11. pip/PyPI installability is a minimum requirement for broad external reuse. TestPyPI is used only for publication validation and is not the official user installation channel. Conda/mamba can be useful for local scientific environments, especially because RDKit is the most platform-sensitive dependency, but conda-forge is an additional future channel rather than a replacement for pip/PyPI readiness.

### Runtime Dependencies

`pyproject.toml` declares minimum runtime dependencies for users and downstream packages:

```text
pandas>=1.5
numpy>=1.23.2
rdkit>=2022.9
```

Exact runtime pins should not live in `project.dependencies` unless there is a strong compatibility reason. Reproducible development or release environments can be documented separately. `scipy` is not a current runtime dependency because CHAMANP does not import it.

### Editable Install From The Repository

```bash
python -m pip install -e .
```

### Local Wheel Or Source Distribution

Build the local distribution artifacts:

```bash
python -m build --no-isolation
```

Install the generated wheel:

```bash
python -m pip install dist/<wheel>.whl
```

or install from the generated source distribution:

```bash
python -m pip install dist/<sdist>.tar.gz
```

### Conda/Mamba Environment For Local Research

For local scientific work, conda/mamba may still be convenient because of RDKit:

```bash
mamba env create -f environment.yml
mamba activate chamanp_env
```

or:

```bash
conda env create -f environment.yml
conda activate chamanp_env
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

The `artifacts/` directory contains local generated outputs and logs. These
files are not versioned as project source files.

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
- `ChamanpConfig`
- `ChamanpResult`
- TOML configuration loading
- public pipeline API doorway
- CLI behavior
- package import safety

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
|-- requirements.txt                  # Legacy/reproducible environment dependency file
|-- requirements-dev.txt              # Development/test dependencies
|-- environment.yml                   # Conda/mamba environment
|-- pyproject.toml                    # Package metadata and canonical runtime dependencies
|-- CHANGELOG.md                      # Development history
|-- chamanp/                          # Package namespace with public API doorways and private internals
|   |-- __init__.py                   # Public package doorway
|   |-- cli.py                        # Minimal public CLI
|   |-- config.py                     # Public configuration object
|   |-- pipeline.py                   # Public validate_config/run doorway
|   |-- result.py                     # Public ChamanpResult object
|   |-- version.py                    # Package version source
|   |-- _core/                        # Private internal pipeline modules
|   |   |-- base_pipeline.py          # Pipeline orchestrator
|   |   |-- curator.py                # Input curation and validation
|   |   |-- filter.py                 # Property and collection-based filtering
|   |   |-- fingerprints.py           # Molecular fingerprint generation
|   |   |-- preflight.py              # Configuration validation before execution
|   |   `-- reporter.py               # Technical report generation
|   `-- _utils/                       # Private internal auxiliary utilities
|       |-- path_manager.py           # Centralized artifact paths
|       |-- result_manager.py         # Report header and file writing
|       `-- collection_utils.py       # Collection taxonomy validation
|-- source_data/
|   |-- README.md                     # Source-data policy
|   |-- coconut_05-2025.csv           # User-provided source database file
|   `-- coconut_taxonomy.json         # Tracked taxonomy reference
`-- artifacts/                        # Generated local output files, ignored by Git
    `-- reports/                      # Execution reports
```

`chamanp/_core/` and `chamanp/_utils/` are private implementation namespaces. They should not be treated as stable public API.

## Development Status

CHAMANP is still in pre-stable development.

- `v0.1.0` established the corrected pre-stable baseline.
- `v0.2.0` focused on centralized project metadata and reproducible report execution metadata.
- `v0.3.0` focused on configuration validation and execution preflight.
- `v0.4.0` established the package foundation and public API doorway.
- `v0.5.0` introduced `ChamanpConfig` as the first public runtime configuration object.
- `v0.6.0` focused on external-facing documentation and the public usability contract.
- `v0.7.0` focused on internal package migration into private namespaces while preserving the current public API.
- `v0.8.0` introduced the public `validate_config(config)` and `run(config)` execution doorway while keeping `Pipeline` private.
- `v0.9.0` introduced `ChamanpResult` as the lightweight structured result returned by `run(config)`.
- `v0.10.0` added TOML configuration profile loading through `ChamanpConfig.from_toml(path)`.
- `v0.11.0` added the minimal public CLI.
- `v0.12.0` validated packaging readiness through local wheel/sdist builds and install smoke checks.
- `v0.13.0` hardened runtime dependency policy, pip/PyPI readiness, and installation documentation.
- `v0.14.0` added pre-release installation validation for local distributions and wheel smoke tests outside the repository checkout.
- `dev-v0.15.0` focused on external publication readiness. The `0.15.0.dev0` distribution was checked with `twine`, uploaded to TestPyPI for publication validation (`https://test.pypi.org/project/chamanp/0.15.0.dev0/`), and installed from a clean external environment with real runtime dependency resolution. TestPyPI is a testing index, not the official user installation channel.
- `dev-v0.16.0` is the stable-release gate cycle. It focuses on release governance, documentation alignment, stable-publication readiness, and deciding how to avoid confusion with historical release metadata before any stable release is declared.

The current package runtime dependency policy is defined in `pyproject.toml`, with minimum dependency ranges intended for users and downstream packages.

Development version metadata uses the PEP 440 `.dev0` format. For example, the
current development cycle reports `0.16.0.dev0`.

## Future Direction

Planned development remains conservative:

- Keep `import chamanp` side-effect free.
- Keep CHAMANP independent from LigandHub while remaining easy for downstream applications, including LigandHub-API, to consume.
- Keep private implementation modules under `chamanp/_core/` and `chamanp/_utils/` out of the public API.
- Preserve the current public execution API contract and evolve it conservatively while keeping heavyweight datasets and fingerprint matrices out of default result objects.
- Keep the CLI and TOML profile support conservative while deferring YAML/JSON configuration profiles, environment configuration, and command-line overrides.
- Continue hardening pip/PyPI installation as a minimum requirement for broad external reuse.
- Reach a stable, publishable release without assuming in advance that the final stable number must be `v1.0.0`.

Future extension areas may include:

- Integration with bioactivity repositories such as ChEMBL or PubChem BioAssay.
- Support for additional fingerprint types and molecular descriptors.
- Broader test coverage and reproducibility metadata.
- Downstream application integration, with LigandHub-API as one possible consumer of CHAMANP.

## Author

Developed by Flavio F. Contreras-Torres, Tecnologico de Monterrey.

## License

This project is licensed under the terms of the [GNU Lesser General Public License v3.0 or later](LICENSE). SPDX identifier: `LGPL-3.0-or-later`.
