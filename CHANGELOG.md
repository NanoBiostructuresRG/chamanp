# Changelog

All notable changes to CHAMANP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## 0.20.1 - 2026-05-28

### Added
- Added GitHub

---

## 0.20.0 - 2026-05-21

### Added
- Added GitHub Pages documentation built with MkDocs, Material for MkDocs, and mkdocstrings.

### Docs
- Added a user-facing input-process-output workflow contract to the README and MkDocs Home page, including how the COCONUT-like example CSV should be interpreted.
- Clarified CHAMANP's taxonomy-backed collection filtering concept, the role of `source_data/coconut_taxonomy.json`, and the project-name analogy to "shaman".
- Added a beginner-facing example execution walkthrough with the TOML profile, CLI commands, expected output, and generated artifacts.
- Grouped documented outputs into essential user-facing artifacts and audit artifacts to reduce confusion about the number of generated files.
- Clarified that TOML profiles are manually written configuration files based on the user's CSV paths, columns, target collections, and output settings.
- Reorganized the MkDocs Home page so installation and the CLI example appear before conceptual sections, removed fragile API anchors, and made citation guidance rely on `CITATION.cff`.
- Polished the MkDocs Home hero, workflow card placement, heading capitalization, and API link style for the final v0.20.0 documentation pass.

### Changed
- Started the documentation aesthetics cycle for the MkDocs site while preserving chemistry behavior and the public API boundary.
- Clarified TOML profile examples so PyPI users are directed to create their own runtime profile instead of relying on a repository-specific example file.
- Collection filtering now accepts both semicolon (`;`) and pipe (`|`) separators in the `collections` field, matching COCONUT-style example data while preserving existing semicolon support.

### Improved
- Improved CI coverage with a Python 3.11/3.12 matrix, public API assertions, wheel smoke installation, source distribution smoke installation, and strict documentation builds.

### Removed
- Removed the repository-specific `examples/chamanp.toml` file from the source tree and source distribution to avoid ambiguity for PyPI users.
- Removed the local PowerShell wheel smoke script and the obsolete `MANIFEST.in`; CI now owns wheel and source distribution smoke validation.
- Removed the internal `DESIGN.md` planning document from the public source tree to keep the PyPI-facing project surface focused on user documentation, API docs, tests, and release notes.
- Removed the internal `INSTALL.md` release checklist; PyPI-facing installation guidance now lives in README and the MkDocs Home page.

---

## 0.19.0 - 2026-05-16

### Docs
- Made CHAMANP's public API understandable through truthful, English, NumPy-style docstrings while preserving the current API boundary and avoiding unrelated infrastructure or behavior changes.
- Updated the README development-status section to reflect the completed 0.18.0 PyPI publication milestone and the current 0.19.0 public API documentation cycle.

---

## 0.18.0 - 2026-05-16

### Added
- Added a manual PyPI Trusted Publishing workflow for the first official pre-stable PyPI publication.

### Changed
- Started the 0.18.0 first official PyPI publication preparation cycle using Trusted Publishing as the intended publication path.
- Kept CHAMANP pre-stable while preparing official PyPI publication without declaring the package stable.

### Docs
- Documented Trusted Publishing setup, GitHub environment configuration, PyPI pending publisher required values, and the first official publication order in `INSTALL.md`.

---

## 0.17.0 - 2026-05-16

### Changed
- Started the 0.17.0 official publication rehearsal and stable-release governance cycle.
- Recorded that the historical `v1.0.0` anomaly was remediated before public stable publication: the GitHub Release was removed manually, the local and remote tags were deleted, and no DOI, Zenodo record, or external release assets were associated with it.

### Docs
- Added stable publication checklist and repository workflow vs. package API boundary documentation to `INSTALL.md`.

---

## 0.16.0 - 2026-05-16

### Added
- Added a versioned GitHub Actions workflow for tests, distribution builds, `twine check`, and wheel smoke-install validation without running the real pipeline.
- Added `.pytest_cache/` to `.gitignore`.

### Changed
- Started the 0.16.0 stable-release gate cycle.
- Changed development version metadata to use the PEP 440-compliant `.dev0` format instead of the previous `-dev` style.
- Updated citation wording so CHAMANP is described as an independent package that may be consumed by LigandHub or other downstream systems.

### Docs
- Aligned DESIGN, README, and INSTALL documentation around release governance before any stable publication.
- Documented the current pre-stable public API contract and clarified that `Pipeline`, `chamanp._core`, and `chamanp._utils` remain private implementation details.
- Clarified that TestPyPI is only a publication-validation index, while official PyPI readiness remains a separate stable-publication requirement.
- Clarified that `artifacts/` contains local generated outputs ignored by Git.

### Removed
- Removed the tracked legacy generated report artifact.
- Removed local `core/__pycache__` and `utils/__pycache__` residue left over from the pre-migration source layout.
- Removed stale `scipy` entries from auxiliary environment files because CHAMANP does not currently use SciPy as a runtime dependency.

---

## 0.15.0 - 2026-05-15

### Changed
- Started PyPI/TestPyPI publication readiness and stable-release contract hardening work after the 0.14.0 pre-release validation cycle.
- Focused the development cycle on distribution publication checks, external install validation, and documenting the stable public contract without changing chemistry behavior, output artifacts, reports, or the public API.

### Tests
- Validated local builds with `twine check`, uploaded `0.15.0.dev0` to TestPyPI for publication validation (`https://test.pypi.org/project/chamanp/0.15.0.dev0/`), and confirmed external clean-environment installation with real runtime dependency resolution.

---

## 0.14.0 - 2026-05-15

### Added
- Added documentation and local smoke-test support for editable installs, wheel installs, source distributions, and the distinction between package runtime dependencies and reproducible local environments.

### Changed
- Started pre-release installation validation work, focused on building CHAMANP distributions and smoke-testing wheel installation outside the repository checkout before v1.0.0.

---

## 0.13.0 - 2026-05-15

### Changed
- Started dependency and installation hardening development, focused on pip/PyPI readiness, packaging portability, and documentation alignment after 0.12.0.
- Treated pip installability as a minimum requirement for broad external reuse; LigandHub-API may be an early downstream consumer, but it is not the design target for CHAMANP.

### Docs
- Clarified installation documentation for editable installs, local wheel/sdist installs, runtime dependency minimums, RDKit installation sensitivity, and CHAMANP's independent package direction.
- Refreshed README development status to align with the current public API, dependency policy, and pip/PyPI readiness focus.

---

## 0.12.0 - 2026-05-15

### Changed
- Started packaging readiness development, focused on distribution metadata, package build validation, and clean-install smoke checks without changing runtime behavior.

### Docs
- Updated documentation so CLI and TOML support are no longer described as future work.

---

## 0.11.0 - 2026-05-15

### Added
- Added a minimal `chamanp` CLI with `--version`, `check-config`, and `run` commands backed by the existing public Python API.

### Changed
- Started CLI development, focused on a minimal public terminal interface for loading TOML profiles, validating configuration, and running CHAMANP through the existing public API.
- Designed the CLI to present clean user-facing errors without Python tracebacks by default.

### Fixed
- CLI command failures now print clean `Error: <message>` output without Python tracebacks by default.

---

## 0.10.0 - 2026-05-14

### Added
- Added `ChamanpConfig.from_toml(path)` using Python 3.11 `tomllib` for external TOML configuration profiles.

### Changed
- Started TOML configuration profile development, focused on loading reproducible external configuration files through `ChamanpConfig.from_toml(path)` without changing pipeline behavior.
- TOML loading accepts lower_snake_case keys, maps them to existing CHAMANP configuration fields, rejects unknown keys, and leaves semantic validation to `validate_config(config)`.

---

## 0.9.0 - 2026-05-14

### Added
- Added public `ChamanpResult` as a frozen dataclass containing execution status, version, artifact paths, fingerprint settings, and summary counts.

### Changed
- Started structured execution result development, focused on returning a public `ChamanpResult` from `run(config)` without changing chemistry behavior, artifact names, output formats, or report contents.
- Updated public `run(config)` to return `ChamanpResult` while preserving existing artifact-writing behavior.
- Kept `Pipeline` private and avoided loading fingerprint matrices, datasets, or reports into the result object.

### Docs
- Documented that `ChamanpResult` reports completed executions and failures remain exception-based.

---

## 0.8.0 - 2026-05-14

### Added
- Added the public execution API doorway, exposing `validate_config` and `run` from the main `chamanp` namespace while keeping `Pipeline` private.
- Added public `validate_config(config)` and `run(config)` exports from the main `chamanp` namespace.

### Changed
- `run(config)` preserves current disk-output behavior and returns `None` in 0.8.0; structured in-memory results are deferred to a future development version.
- Kept `Pipeline` private and out of `chamanp.__all__`.

### Docs
- Documented that `run(config)` returns `None` in 0.8.0 and writes configured artifacts to disk.

### Internal
- No chemistry, fingerprint, artifact, output, or report behavior changes were intended.

---

## 0.7.0 - 2026-05-14

### Added
- Added private internal namespaces under `chamanp/_core` and `chamanp/_utils`.

### Changed
- Completed the internal package migration for private `chamanp/_core` and `chamanp/_utils` namespaces, import-safety hardening, and a clean migration away from root-level `core/` and `utils` without changing chemistry behavior, outputs, artifacts, or reports.
- Kept the current public API as `from chamanp import __version__, ChamanpConfig`; `Pipeline` remains internal and is not publicly exported.
- Moved internal utility modules into `chamanp/_utils`.
- Moved internal core pipeline modules into `chamanp/_core`.
- Deferred pipeline logging setup until execution so importing pipeline internals no longer creates `artifacts/` or `artifacts/pipeline.log`.

### Removed
- Removed the root-level `core/version.py` compatibility bridge after package metadata moved fully to `chamanp.version`.

### Internal
- No chemistry, output, artifact, or report behavior changes were intended in this migration.

---

## 0.6.0 - 2026-05-14

### Added
- Added `DESIGN.md` as an internal strategic design reference for CHAMANP identity, public API direction, COCONUT-as-reference-dataset scope, and roadmap.

### Changed
- Started the external-facing documentation cycle, focused on CHAMANP's public usability contract without changing chemical processing behavior.

### Docs
- Rewrote README from an external user perspective, clarifying CHAMANP's purpose, current usable modes, COCONUT-as-reference-dataset scope, and current public API boundaries.

---

## 0.5.0 - 2026-05-14

### Added
- Added `ChamanpConfig` as the first public runtime configuration object, with no chemical processing behavior changes.

### Changed
- Started the configuration API development cycle, focused on introducing a public runtime configuration object for CHAMANP without changing chemical processing behavior.

---

## 0.4.0 - 2026-05-13

### Added
- Added minimal package metadata in `pyproject.toml`.
- Added a minimal `chamanp` package namespace exposing `__version__`.
- Added package import smoke tests that do not run the pipeline or require source data.

### Changed
- Changed project license metadata from MIT to `LGPL-3.0-or-later` by project-owner decision.

### Docs
- Documented the package transition direction and draft future public API.

### Internal
- No chemical curation, SMILES validation, collection filtering, fingerprint generation, reporting, or artifact naming changes were intended in this development pass.

---

## 0.3.0 - 2026-05-13

### Added
- Added configuration preflight validation before pipeline execution.
- Added `ConfigurationError` for clear early failures when required config values are missing or invalid.
- Added focused tests for preflight validation and entrypoint ordering.

### Changed
- Validated configured database and collection taxonomy paths before entering curation or fingerprint generation.
- Validated target collections, collection logic, safe collection tags, and Morgan fingerprint parameters.
- Hardened `TARGET_COLLECTIONS` validation to require a non-empty collection of non-empty strings.

### Removed
- Removed unused `OUTPUT_PATH` from `config.py`.

### Internal
- No chemical curation, SMILES validation, collection filtering, or fingerprint generation logic changes were intended in this development pass.

---

## 0.2.0 - 2026-05-13

### Added
- Added centralized project metadata in `core/version.py`.
- Added future report execution metadata for input CSV path, collection tag, fingerprint radius, fingerprint bit length, and valid fingerprinted molecule count.
- Added tests to ensure report headers include centralized metadata and do not contain the legacy `v1.0` version string.

### Changed
- Updated future report headers to use centralized CHAMANP version/status metadata.

### Removed
- Removed the legacy hardcoded `v1.0 - May, 2025. Oviedo` report header for future reports.

### Internal
- No chemical curation, collection filtering, or fingerprint generation logic changes were intended in this development pass.

---

## 0.1.0 - 2026-05-13

### Added
- Added invalid SMILES traceability during fingerprint generation.
- Added `invalid_smiles_{tag}.csv` output through `PathManager` and `Pipeline`.
- Added tests for substring non-match, semicolon-separated labels, whitespace handling, and missing/NaN values.
- Added reporter tests and fingerprint count assertions.

### Changed
- Preserved existing valid fingerprint and valid metadata outputs.
- Replaced substring-based collection filtering with exact label matching.
- Parsed collections as semicolon-separated labels with surrounding whitespace stripped.
- Kept missing/NaN collection values from matching.
- Updated tests; current validation was 29 tests passing.

### Docs
- Reports now include invalid SMILES count/path when provided by the pipeline.

### Internal
- `FingerprintGenerator` exposes `invalid_smiles_count` for report traceability.
- `ReportWriter` remains backward-compatible when invalid fields are omitted.

---

## 1.0.1-dev - 2026-05-12

### Changed
- Kept CHAMANP as a pre-stable development prototype.
- Prepared the project toward a corrected `0.1.0`-style baseline by documenting the runtime environment, clarifying source-data expectations, and softening earlier stable-version language.
- Kept the baseline free of intended pipeline behavior changes.

### Tests
- Added baseline tests for isolated non-RDKit components: `path_manager`, `collection_utils`, and `filter`.
- Added baseline tests for isolated RDKit-related components: `curator` and `fingerprints`.
- Current validation was 21 tests passing.
