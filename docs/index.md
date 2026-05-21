# CHAMANP

<section class="cp-hero">
  <div class="cp-hero__content">
    <p class="cp-eyebrow">Natural products curation</p>
    <div class="cp-brand" aria-label="CHAMANP">
      <span class="cp-dotmark" aria-hidden="true">
        <span></span><span></span><span></span>
        <span></span><span></span><span></span>
        <span></span><span></span><span></span>
      </span>
      <span class="cp-wordmark">CHAMANP</span>
    </div>
    <p class="cp-subtitle">
      Curation and Hierarchical Analysis for Molecular Annotation of Natural Products.
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


<section class="cp-panel">
  <div class="cp-grid cp-grid--three">
    <article class="cp-card">
      <span class="cp-card__icon">01</span>
      <h3>Validate first</h3>
      <p>Catch configuration problems before chemical processing begins.</p>
    </article>
    <article class="cp-card">
      <span class="cp-card__icon">02</span>
      <h3>Curate traces</h3>
      <p>Keep curated tables, filtered subsets, invalid SMILES, and reports aligned.</p>
    </article>
    <article class="cp-card">
      <span class="cp-card__icon">03</span>
      <h3>Export fingerprints</h3>
      <p>Generate RDKit Morgan fingerprints with reproducible artifact names.</p>
    </article>
  </div>
</section>

## Why CHAMANP?

**CHAMANP** fills the gap between raw molecular databases and analysis-ready
datasets for cheminformatics or machine learning pipelines. Current development
uses [COCONUT](https://coconut.naturalproducts.net/) as the reference dataset.

!!! tip "Dataset preparation contract"
    CHAMANP keeps molecular dataset preparation traceable: configuration is
    validated before execution, curated and filtered tables are written as
    artifacts, invalid SMILES are recorded, and RDKit Morgan fingerprints are
    exported with reproducible names.

## Installation

```bash
pip install chamanp
```

CHAMANP requires Python 3.11 or 3.12 and depends on
[RDKit](https://www.rdkit.org/), pandas, and numpy.

## Quick Start

=== "ChamanpConfig"

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

=== "validate_config"

    ```python
    from chamanp import ChamanpConfig, validate_config

    cfg = ChamanpConfig.from_toml("examples/chamanp.toml")
    validate_config(cfg)
    ```

=== "run"

    ```python
    from chamanp import ChamanpConfig, run

    cfg = ChamanpConfig.from_toml("examples/chamanp.toml")
    result = run(cfg)
    print(result.valid_molecules_count)
    print(result.fingerprints_path)
    ```

=== "ChamanpResult"

    ```python
    from chamanp import ChamanpConfig, ChamanpResult, run

    cfg = ChamanpConfig.from_toml("examples/chamanp.toml")
    result = run(cfg)

    assert isinstance(result, ChamanpResult)
    print(result.status)
    print(result.report_path)
    ```

### CLI

```bash
chamanp --version
chamanp check-config examples/chamanp.toml
chamanp run examples/chamanp.toml
```

## Public API

| Symbol | Description |
|--------|-------------|
| [`ChamanpConfig`](api.md#chamanpconfig) | Runtime configuration object |
| [`ChamanpResult`](api.md#chamanpresult) | Lightweight result returned by `run()` |
| [`validate_config`](api.md#validate_config) | Validate configuration before execution |
| [`run`](api.md#run) | Execute the CHAMANP pipeline |
| `__version__` | Package version string |

## Citation

```text
Contreras-Torres, F. F. (2026). CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products (v0.19.0). Zenodo. https://doi.org/10.5281/zenodo.20249166
```

## License

This project is licensed under the terms of the
[GNU Lesser General Public License v3.0 or later](https://github.com/NanoBiostructuresRG/chamanp/blob/main/LICENSE).
SPDX identifier: `LGPL-3.0-or-later`.
