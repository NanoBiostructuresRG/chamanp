
# CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products
**Version 1.0.0 – Oviedo**

---

## Description
**CHAMANP** is a modular, extensible, and production-grade system for the curated preparation of molecular databases.
Designed to process over 50 annotated natural product collections from the COCONUT dataset, CHAMANP enables rigorous, scalable, and reproducible data preparation for cheminformatics applications. 
The framework is particularly suited to pharmaceutical and natural products research, where thematic organization of compounds libraries is essential for identifying novel bioactive leads.
CHAMANP is developed following high-standards in object-oriented programming and scientific software development.

---

## Purpose
The primary objective of CHAMANP is to support the systematic and reproducible preparation of curated molecular datasets. The platform enables:
- Standardized curation and deduplication of chemical structures.
- Semantic filtering of compounds based on biological taxonomy and physicochemical properties.
- Generation of machine learning–ready molecular fingerprints.
- Production of traceable, report-driven documentation for downstream analysis.

---

## Project Structure
```text
chamanp/
├── main.py                          # Pipeline entry point
├── config.py                        # Global system configuration
│
├── core/                            # Core components of the pipeline
│   ├── base_pipeline.py             # Main pipeline orchestrator class
│   ├── curator.py                   # Input curation and validation
│   ├── filter.py                    # Property and collection-based filtering
│   ├── fingerprints.py              # Molecular fingerprint generation
│   └── reporter.py                  # Technical report generation
│
├── utils/                           # Auxiliary tools and utilities
│   ├── path_manager.py              # Centralized path generation logic
│   ├── result_manager.py            # Report header and file writing
│   └── collection_utils.py          # Semantic validation of collections
│
├── source_data/                     # Source files (JSON + CSV)
│   ├── coconut_05-2025.csv
│   └── coconut_taxonomy.json
│
├── artifacts/                       # Automatically generated output files
│   ├── reports/                     # Execution reports with formal headers
│   ├── *.csv                        # Curated and filtered compound datasets
│   ├── *.npy                        # Molecular fingerprints
│   └── *.log                        # Execution logs
│
└──README.md                         # This file
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

