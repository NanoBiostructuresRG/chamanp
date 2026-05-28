# CHAMANP: Curation and Hierarchical Analysis for Molecular Annotation of Natural Products

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.20.1-blue.svg)](https://pypi.org/project/chamanp/)
[![PyPI](https://img.shields.io/pypi/v/chamanp.svg)](https://pypi.org/project/chamanp/)
[![Python](https://img.shields.io/pypi/pyversions/chamanp.svg)](https://pypi.org/project/chamanp/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-teal.svg)](https://nanobiostructuresrg.github.io/chamanp/)

**CHAMANP** is a pre-stable Python package for systematic, reproducible
curation and preparation of natural-product molecular datasets.

It sits between raw molecular tables and analysis-ready cheminformatics or
machine-learning inputs. Current development uses COCONUT-style data as the
reference workflow, but CHAMANP is intended to remain reusable for other
tabular natural-product sources with SMILES and collection metadata.

The name intentionally echoes "shaman": CHAMANP interprets a molecular table
through a collection taxonomy, helping users separate compounds that belong to
one or several source collections.

## Status

CHAMANP is published as an Alpha-stage, pre-stable package. The current public
API is usable, but the project is still hardening its documentation contract,
release workflow, and stable public boundary.

The current public package doorway is:

```python
from chamanp import ChamanpConfig, ChamanpResult, validate_config, run
```

The minimal CLI is available as:

```bash
chamanp --version
chamanp check-config my-chamanp-profile.toml
chamanp run my-chamanp-profile.toml
python -m chamanp --version
```

`Pipeline`, `chamanp._core`, and `chamanp._utils` are private implementation
details and should not be treated as stable public API.

## Install

```bash
pip install chamanp
```

CHAMANP targets Python 3.11 and 3.12. Runtime dependencies are declared in
`pyproject.toml` and include pandas, numpy, and RDKit. RDKit is the most
platform-sensitive dependency; conda/mamba may still be useful for local
scientific environments.

## Documentation

The full user documentation is published with MkDocs Material:

- [Home](https://nanobiostructuresrg.github.io/chamanp/) introduces the project,
  dataset contract, taxonomy concept, citation, and license.
- [Usage](https://nanobiostructuresrg.github.io/chamanp/usage/) covers
  installation, CLI usage, TOML profiles, and Python examples.
- [API Reference](https://nanobiostructuresrg.github.io/chamanp/api/) documents
  the current public API generated with `mkdocstrings`.
- [Changelog](https://nanobiostructuresrg.github.io/chamanp/changelog/)
  records release notes.

This README is intentionally concise. Detailed examples, TOML profile guidance,
and API examples live in the documentation site.

## What CHAMANP Does

At a high level, CHAMANP can:

- validate configuration before chemical processing begins;
- curate SMILES with RDKit;
- filter compounds by exact collection labels from a taxonomy;
- handle duplicate structures and optional stereochemistry-related duplicate
  removal;
- generate RDKit Morgan fingerprints;
- record invalid SMILES rows for traceability;
- write curated tables, filtered tables, valid-molecule metadata, fingerprint
  matrices, and preparation reports.

CHAMANP does not currently provide molecular property prediction, docking,
virtual screening, or a stable public API.

## Minimal Orientation

A typical run starts from:

- a CSV table with `canonical_smiles`, `collections`, and selected metadata
  columns;
- a collection taxonomy JSON file;
- a TOML profile or `ChamanpConfig` with input paths, target collections,
  fingerprint settings, selected columns, and output locations.

The recommended user path is documented in the
[Usage page](https://nanobiostructuresrg.github.io/chamanp/usage/). Source
checkouts also include `examples/example_chamanp.csv` and
`source_data/coconut_taxonomy.json` for the reference walkthrough.

## Repository Structure

```text
CHAMANP/
|-- chamanp/                 # Package namespace and public API doorway
|   |-- __init__.py          # Public exports
|   |-- __main__.py          # python -m chamanp entry point
|   |-- cli.py               # Minimal public CLI
|   |-- config.py            # ChamanpConfig
|   |-- pipeline.py          # validate_config/run doorway
|   |-- result.py            # ChamanpResult
|   |-- version.py           # Package version source
|   |-- _core/               # Private pipeline implementation
|   `-- _utils/              # Private utilities
|-- docs/                    # MkDocs Material documentation
|-- examples/                # Small example input data
|-- source_data/             # Source-data policy and taxonomy reference
|-- tests/                   # Focused tests
|-- main.py                  # Repository workflow entry point
|-- pyproject.toml           # Package metadata and dependencies
|-- CHANGELOG.md             # Release notes
|-- CITATION.cff             # Citation metadata
`-- README.md                # Repository overview
```

Generated outputs are written under `artifacts/`, which is ignored by Git.

## Development

Install the package in editable mode from a source checkout:

```bash
python -m pip install -e ".[dev,docs]"
```

Build the documentation:

```bash
mkdocs build --strict
```

Run tests:

```bash
python -m pytest tests
```

The CI workflow runs tests, package build checks, smoke installs, CLI checks,
and a strict documentation build. The documentation deployment workflow publishes
the MkDocs site to GitHub Pages.

## Citation

Use `CITATION.cff` as the authoritative machine-readable citation metadata.
Citation metadata is updated with each release.

## License

This project is licensed under the terms of the
[GNU Lesser General Public License v3.0 or later](LICENSE).
SPDX identifier: `LGPL-3.0-or-later`.
