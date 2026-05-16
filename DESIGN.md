# CHAMANP Strategic Design Document

**Version:** draft-v0.16.0
**Status:** Internal reference. Not part of the public API.
**Author:** Flavio F. Contreras-Torres, Tecnologico de Monterrey

---

## 1. Identity

CHAMANP is a Python engine for the systematic, reproducible curation and
preparation of molecular datasets of natural products.

Its full name, **Curation and Hierarchical Analysis for Molecular Annotation of
Natural Products**, defines its scope:

- It curates and prepares molecular datasets.
- It works in the natural products domain.
- It produces annotated, analysis-ready artifacts.

CHAMANP is not a wrapper around a single database. It is intended to operate on
natural product molecular databases that can be represented as tabular files
with SMILES strings and collection metadata.

---

## 2. The Problem CHAMANP Solves

Researchers in cheminformatics, drug discovery, drug repositioning, nutrition,
biomedicine, and nutraceutics routinely need curated, reproducible molecular
datasets before analysis or machine learning workflows can begin.

Today, many researchers solve this problem with ad hoc scripts:

- Written once, hard to reuse.
- No validation before execution.
- No traceability of what was filtered or why.
- No consistent artifact naming.
- No reproducibility across runs or collaborators.

CHAMANP replaces the ad hoc script with a configurable, testable, traceable
curation and preparation pipeline.

---

## 3. Target Users

CHAMANP is designed for users working at the intersection of molecular data and
computational analysis:

- Cheminformatics researchers preparing datasets for analysis or publication.
- Drug discovery and repositioning groups working with natural product libraries.
- Nutrition, biomedicine, and nutraceutics researchers curating compound sets.
- Computational labs integrating molecular curation into reproducible workflows.
- Developers building notebooks, pipelines, servers, or applications that need a
  reusable molecular dataset preparation engine.

CHAMANP is an independent package. It should remain useful to scientists,
notebooks, pipelines, servers, and external applications outside any single
downstream project. LigandHub-API may become an early real downstream consumer
through pip installation in Docker, but it must not define CHAMANP's identity,
public API, or package design.

---

## 4. Design Philosophy

### 4.1 General Natural Product Datasets, Not One Database

CHAMANP is designed to work with natural product molecular databases that can be
represented as tabular files with SMILES strings and collection metadata.

COCONUT is the current reference dataset used during development. It is not the
only intended dataset, and it must not become a permanent hardcoded assumption in
APIs that claim to be generic.

CHAMANP should avoid silently hardcoding COCONUT-specific assumptions into a
supposedly reusable interface. Any COCONUT-specific defaults should be clearly
identified as defaults, examples, or reference-data behavior.

### 4.2 Configuration First

Pipeline behavior should be represented through explicit configuration, not
hidden global state. The first public configuration contract is
`ChamanpConfig`.

The legacy repository-level `config.py` remains part of the current repository
workflow, while external consumers can configure CHAMANP through package-level
objects and functions.

### 4.3 Fail Early, Fail Clearly

CHAMANP validates configuration before computation begins. Missing paths,
malformed collection settings, unsafe artifact tags, or invalid fingerprint
parameters should fail with clear errors before curation, filtering,
fingerprinting, or reporting starts.

### 4.4 Traceable By Default

Pipeline runs should produce consistently named artifacts, execution reports,
and invalid SMILES traceability. Reproducibility should be a default property of
the workflow, not an afterthought.

### 4.5 Import-Safe

Importing `chamanp` must remain side-effect free. Importing the package should
not create directories, write files, configure logging, load source datasets, or
run any part of the pipeline.

Side effects should occur only when the user explicitly requests execution.

---

## 5. Reference Dataset: COCONUT

During active development, CHAMANP uses COCONUT, the COlleCtion of Open NatUral
producTs, as its reference dataset.

COCONUT provides:

- A large, open, tabular molecular database of natural products.
- Collection metadata that enables filtering.
- SMILES representations for compounds.

The collection taxonomy used by CHAMANP, `coconut_taxonomy.json`, was prepared
for the current reference workflow. It is a tracked project artifact, not a
general requirement for all future datasets.

Future work should make dataset-specific assumptions explicit and should support
onboarding other natural product datasets with equivalent or adapted metadata.

---

## 6. Current Public API

The current pre-stable public package contract is:

```python
from chamanp import __version__, ChamanpConfig, validate_config, run, ChamanpResult
```

| Symbol | Type | Purpose |
|---|---|---|
| `__version__` | `str` | Package version |
| `ChamanpConfig` | dataclass | Public runtime configuration contract |
| `ChamanpResult` | frozen dataclass | Lightweight execution result containing artifact paths and summary counts |
| `validate_config` | function | Public validation entrypoint for runtime configuration |
| `run` | function | Public execution entrypoint over the private pipeline implementation |

Implementation internals now live under private package namespaces,
`chamanp._core` and `chamanp._utils`. `Pipeline` remains private and is not part
of the public `chamanp` API. External consumers should not rely on direct imports
from `chamanp._core`, `chamanp._utils`, or `Pipeline`; those names may change
outside the stable public contract.

---

## 7. Public Execution Contract

The public execution doorway is implemented through `validate_config(config)`
and `run(config)`:

```python
from chamanp import ChamanpConfig, ChamanpResult, validate_config, run

config = ChamanpConfig(
    DATABASE_PATH="path/to/database.csv",
    COLLECTION_TAXONOMY_PATH="path/to/taxonomy.json",
    TARGET_COLLECTIONS=["PubChem NPs"],
    COLLECTION_TAG="pubchem",
    COLLECTION_LOGIC="OR",
    MORGAN_RADIUS=2,
    MORGAN_BITS=1024,
)

validate_config(config)
result = run(config)
assert isinstance(result, ChamanpResult)
```

`run(config)` preserves disk-output behavior and returns a lightweight
`ChamanpResult`. The result object reports completed executions and artifact
paths without loading datasets, fingerprint matrices, or reports into memory.
Execution failures remain exception-based.

The public API should hide internal implementation details. Consumers should
not need to import directly from `core/`, `utils/`, `chamanp._core`, or
`chamanp._utils`.

---

## 8. Release Governance And Roadmap

CHAMANP is being prepared for a future stable, publishable release. The stable
release number is intentionally not fixed here. It may be `v1.0.0` or another
appropriate version number, depending on release governance, package index
state, and the cleanup needed before public stability is declared.

The historical `v1.0.0` tag from May 2025 predates the current package
structure, public API, and pre-stable release sequence. It should be treated as
a historical anomaly, not as evidence of a stable CHAMANP package contract.
Before any stable publication, the project should make that history clear enough
that users are not confused about which release represents the stable package.

| Version | Theme | Key Deliverable |
|---|---|---|
| v0.4.0 | Package foundation | Minimal `chamanp` namespace and package metadata |
| v0.5.0 | Configuration contract | `ChamanpConfig` as first public runtime configuration object |
| v0.6.0 | External usability | README rewritten for external users and public usability contract |
| v0.7.0 | Internal package migration | Move internals into private `chamanp/_core` and `chamanp/_utils` paths |
| v0.8.0 | Public execution API | Import-safe public execution entrypoint |
| v0.9.0 | Structured execution result | Public `ChamanpResult` returned by `run(config)` |
| v0.10.0 | TOML profile loading | External TOML configuration profiles through `ChamanpConfig.from_toml(path)` |
| v0.11.0 | Minimal CLI | Public `chamanp --version`, `chamanp check-config`, and `chamanp run` commands |
| v0.12.0 | Packaging readiness | Build validation, distribution metadata, and clean-install smoke checks |
| v0.13.0 | Dependency hardening | pip/PyPI readiness, packaging portability, and dependency policy cleanup |
| v0.14.0 | Install validation | Local distribution install smoke checks outside the repository checkout |
| v0.15.0 | External publication readiness | TestPyPI validation and external dependency-resolution checks |
| dev-v0.16.0 | Stable-release gate | Release governance, CI readiness, documentation alignment, and stable-publication checklist |
| Future stable release | Stable public API | Stable package API and official publication target |

---

## 9. Structural Migration Status

The v0.7.0 migration retired root-level `core/` and `utils/` from tracked
source. Runtime implementation internals now live inside the package namespace
under private paths:

```text
chamanp/_core/
chamanp/_utils/
```

The underscore prefix marks these as private subpackages. External consumers
should use public imports exposed by `chamanp`, not private implementation
paths.

Import-safety has also been improved: importing `chamanp` does not load the
private pipeline implementation, create `artifacts/`, or configure
`artifacts/pipeline.log`. `Pipeline` remains private. Public execution is now
available through the `validate_config(config)` and `run(config)` package
functions, plus the minimal `chamanp` CLI.

---

## 10. What CHAMANP Is Not

- CHAMANP is not a molecular property predictor.
- CHAMANP is not a docking or virtual screening tool.
- CHAMANP is not a database. It prepares data from databases.
- CHAMANP is not COCONUT-specific. COCONUT is the current reference dataset.
- CHAMANP is not a component of LigandHub. LigandHub-API may consume CHAMANP,
  but it does not define CHAMANP's identity or public contract.
- `Pipeline`, `chamanp._core`, and `chamanp._utils` are private implementation
  details, not stable public API.

---

## 11. Deferred Decisions

The current public execution API shape is no longer deferred. The current
contract is `__version__`, `ChamanpConfig`, `validate_config`, `run`, and
`ChamanpResult` from the top-level `chamanp` namespace.

The following decisions remain intentionally deferred:

- CLI extensions beyond the minimal public commands.
- YAML/JSON configuration profiles.
- Environment variables, command-line overrides, and multiple named profiles.
- Automated taxonomy construction.
- Additional public result formats beyond the current lightweight
  `ChamanpResult` contract.
- Conda-forge packaging details.

pip/PyPI installability is no longer deferred: it is a minimum requirement for
broad external reuse. Conda-forge may become an additional distribution channel
later, but it should not replace the pip/PyPI goal.

---

*This internal design reference should be updated at major design boundaries. It
does not replace user documentation, API documentation, tests, or release notes.*
