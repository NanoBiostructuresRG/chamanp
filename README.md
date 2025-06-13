
# CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products
**Version 1.0.0 – May, 2025. Oviedo**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Version](https://img.shields.io/badge/version-v1.0-blue.svg)]()

---

## Description
**CHAMANP** is a modular, extensible, and production-grade framework for the curated preparation of molecular databases. It is implemented following high-standards of object-oriented programming and is designed to process over 50 annotated natural product collections derived from the COCONUT dataset. 

---

## Purpose
The primary objective of CHAMANP is to support the systematic and reproducible preparation of curated molecular datasets for cheminformatics workflows and **phase 3** machine learning applications within the computational drug discovery pipeline. The framework is particularly suited to pharmaceutical and natural products research, where thematic organization of compounds libraries is essential for identifying novel bioactive leads. The platform enables:

- **Standardized curation and deduplication** of chemical structures.
- **Semantic filtering** of compounds based on biological taxonomy and physicochemical properties.
- **Generation of molecular fingerprints** for machine learning applications.
- **Production of traceable, report-driven documentation** for downstream analysis.

---

## Project Structure
```text
CHAMANP/Phase 3
│
├── main.py                           # Entry point
├── config.py                         # Global system configuration
│
├── core/                             # Pipeline
│   ├── base_pipeline.py              # Main pipeline orchestrator class
│   ├── curator.py                    # Input curation and validation
│   ├── filter.py                     # Property and collection-based filtering
│   ├── fingerprints.py               # Molecular fingerprint generation
│   └── reporter.py                   # Technical report generation
│
├── utils/                            # Auxiliary
│   ├── path_manager.py               # Centralized path generation logic
│   ├── result_manager.py             # Report header and file writing
│   └── collection_utils.py           # Semantic validation of collections
│
├── source_data/                      
│   ├── coconut_05-2025.csv           # Source database file
│   └── coconut_taxonomy.json         # Taxonomy dataset
│
├── artifacts/                        # Automatically generated output files
│   ├── reports/                      # Execution reports with formal headers
│   ├── pipeline.log                  # Execution logs
│   ├── X_{tag}.npy                   # Output - molecular fingerprints
│   └── valid_metadata_{tag}.csv      # Output - curated and filtered compound datasets
│
└──README.md                          # This file
```

---

## How to Run
From the project root directory, run:

```bash
python main.py
```

This will execute the full pipeline: input curation → filtering → fingerprinting → reporting.

---

## Preparation

Ensure that your input file inside `source_data/` includes the following fields:

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

To ignore stereochemistry in SMILES during deduplication, set:

```python
REMOVE_STEREO_DUPLICATES = True
```

To filter compounds based on specific COCONUT collections, set:

```python
TARGET_COLLECTIONS = ["ChEMBL NPs"]
COLLECTION_TAG = "chembl"
```

---

## Output

The following files will be saved under the `artifacts/` directory:

- `curated_*.csv`  
- `filtered_*.csv`  
- `valid_metadata_*.csv`  
- `X_*.npy`  
- `report_phase2_*.txt`  
- `pipeline.log`

---

## Example Console Output

```text
[INFO] Total compounds after filtering: 1447
[INFO] Generating molecular fingerprints...
[INFO] Fingerprints and metadata saved.
[INFO] Generating final report...
[INFO] Report saved to: artifacts/reports/report_phase2_chembl.txt
[INFO] Pipeline execution completed.
```

---

## Key Features

- Fully modular and object-oriented design.
- Automated curation, filtering, and fingerprint generation.
- Reproducible reports with standardized institutional headers.
- Robust collection validation with structured error handling.
- Professional logging: console output and persistent `.log` file.

---

## Future Extensions

- **Integration with Bioactivity Data Repositories**  
  Enable direct annotation from ChEMBL or PubChem BioAssay to support SAR modeling.

- **Support for Additional Fingerprint Types and Descriptors**  
  Extend to include ECFP6, MACCS keys, or 3D-based descriptors for advanced modeling.

---

## Author

Developed by **Flavio F. Contreras-Torres** (Tecnológico de Monterrey)  
Oviedo, Spain – May 2025

---

## License

This project is licensed under the terms of the [MIT License](https://github.com/NanoBiostructuresRG/chamanp/blob/main/LICENSE).  
See the LICENSE file for full details.
