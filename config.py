# config.py

DATABASE_PATH = "source_data/coconut_05-2025.csv"

REPORTS_PATH = "artifacts/reports"

COLLECTION_TAXONOMY_PATH = "source_data/coconut_taxonomy.json"

TARGET_COLLECTIONS = ["PubChem NPs"]

COLLECTION_TAG = "pubchem"

COLLECTION_LOGIC = "OR"

MORGAN_RADIUS = 2

MORGAN_BITS = 1024

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

REMOVE_STEREO_DUPLICATES = True

