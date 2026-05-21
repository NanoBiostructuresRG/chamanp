# CHAMANP

**Curation and Hierarchical Analysis for Molecular Annotation of Natural Products**

[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL_v3%2B-blue.svg)](https://github.com/NanoBiostructuresRG/chamanp/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/chamanp)](https://pypi.org/project/chamanp/)
[![Python](https://img.shields.io/pypi/pyversions/chamanp)](https://pypi.org/project/chamanp/)
[![CI](https://github.com/NanoBiostructuresRG/chamanp/actions/workflows/ci.yml/badge.svg)](https://github.com/NanoBiostructuresRG/chamanp/actions/workflows/ci.yml)

---

CHAMANP is a Python library for systematic, reproducible curation and
preparation of molecular datasets of natural products.

It fills the gap between raw molecular databases and analysis-ready datasets
for cheminformatics or machine learning pipelines. Current development uses
[COCONUT](https://coconut.naturalproducts.net/) as the reference dataset.

!!! note "Pre-stable"
    CHAMANP is currently in Alpha-stage development. The public API is being
    hardened before stability is declared.

---

## Why CHAMANP?

Researchers often prepare molecular datasets with ad hoc scripts that are
difficult to validate, repeat, or share. CHAMANP provides a more reproducible
preparation workflow:

- Early configuration validation before chemical processing begins.
- Collection-based filtering for natural product subsets.
- RDKit Morgan fingerprint generation.
- Invalid SMILES traceability.
- Consistent output artifacts and preparation reports.
- Better reproducibility across runs, collaborators, and downstream analyses.

---

## Installation

```bash
pip install chamanp
```

CHAMANP requires Python 3.11 or 3.12 and depends on
[RDKit](https://www.rdkit.org/), pandas, and numpy.

---

## Quickstart

### Create a configuration object

```python
from chamanp import ChamanpConfig, validate_config, run

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

validate_config(cfg)
result = run(cfg)
print(result.valid_molecules_count)
```

### Load a TOML profile

```python
from chamanp import ChamanpConfig, validate_config, run

cfg = ChamanpConfig.from_toml("examples/chamanp.toml")
validate_config(cfg)
result = run(cfg)
```

### Use the CLI

```bash
chamanp --version
chamanp check-config examples/chamanp.toml
chamanp run examples/chamanp.toml
```

---

## Public API

| Symbol | Description |
|--------|-------------|
| [`ChamanpConfig`](api.md#chamanp.config.ChamanpConfig) | Runtime configuration object |
| [`ChamanpResult`](api.md#chamanp.result.ChamanpResult) | Lightweight result returned by `run()` |
| [`validate_config`](api.md#chamanp.pipeline.validate_config) | Validate configuration before execution |
| [`run`](api.md#chamanp.pipeline.run) | Execute the CHAMANP pipeline |
| `__version__` | Package version string |

---

## License

LGPL-3.0-or-later — see
[LICENSE](https://github.com/NanoBiostructuresRG/chamanp/blob/main/LICENSE).

Developed by Flavio F. Contreras-Torres, Tecnologico de Monterrey.
