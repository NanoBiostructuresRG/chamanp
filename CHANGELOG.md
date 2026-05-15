# Changelog

## [dev-v0.11.0] - Unreleased

- Started CLI development, focused on a minimal public terminal interface for loading TOML profiles, validating configuration, and running CHAMANP through the existing public API.
- The planned CLI should present clean user-facing errors without Python tracebacks by default.

## [v0.10.0] - 2026-05-14

- Started TOML configuration profile development, focused on loading reproducible external configuration files through `ChamanpConfig.from_toml(path)` without changing pipeline behavior.
- Added `ChamanpConfig.from_toml(path)` using Python 3.11 `tomllib` for external TOML configuration profiles.
- TOML loading accepts lower_snake_case keys, maps them to existing CHAMANP configuration fields, rejects unknown keys, and leaves semantic validation to `validate_config(config)`.

## [v0.9.0] - 2026-05-14

- Started structured execution result development, focused on returning a public `ChamanpResult` from `run(config)` without changing chemistry behavior, artifact names, output formats, or report contents.
- Added public `ChamanpResult` as a frozen dataclass containing execution status, version, artifact paths, fingerprint settings, and summary counts.
- Updated public `run(config)` to return `ChamanpResult` while preserving existing artifact-writing behavior.
- Kept `Pipeline` private and avoided loading fingerprint matrices, datasets, or reports into the result object.
- Documented that `ChamanpResult` reports completed executions and failures remain exception-based.

## [v0.8.0] - 2026-05-14

- Added the public execution API doorway, exposing `validate_config` and `run` from the main `chamanp` namespace while keeping `Pipeline` private.
- `run(config)` preserves current disk-output behavior and returns `None` in v0.8.0; structured in-memory results are deferred to a future development version.
- No chemistry, fingerprint, artifact, output, or report behavior changes are intended.
- Added public `validate_config(config)` and `run(config)` exports from the main `chamanp` namespace.
- Kept `Pipeline` private and out of `chamanp.__all__`.
- Documented that `run(config)` returns `None` in v0.8.0 and writes configured artifacts to disk.

## [v0.7.0] - 2026-05-14

- Completed the internal package migration for private `chamanp/_core` and `chamanp/_utils` namespaces, import-safety hardening, and a clean migration away from root-level `core/` and `utils/` without changing chemistry behavior, outputs, artifacts, or reports.
- The current public API remains `from chamanp import __version__, ChamanpConfig`; `Pipeline` remains internal and is not publicly exported.
- Added private internal namespaces under `chamanp/_core` and `chamanp/_utils`.
- Moved internal utility modules into `chamanp/_utils`.
- Moved internal core pipeline modules into `chamanp/_core`.
- Deferred pipeline logging setup until execution so importing pipeline internals no longer creates `artifacts/` or `artifacts/pipeline.log`.
- Removed the root-level `core/version.py` compatibility bridge after package metadata moved fully to `chamanp.version`.
- No chemistry, output, artifact, or report behavior changes are intended in this migration.

## [v0.6.0] - 2026-05-14

- Started the external-facing documentation cycle, focused on CHAMANP's public usability contract without changing chemical processing behavior.
- Added `DESIGN.md` as an internal strategic design reference for CHAMANP identity, public API direction, COCONUT-as-reference-dataset scope, and roadmap.
- Rewrote README from an external user perspective, clarifying CHAMANP's purpose, current usable modes, COCONUT-as-reference-dataset scope, and current public API boundaries.

## [v0.5.0] - 2026-05-14

- Started the configuration API development cycle, focused on introducing a public runtime configuration object for CHAMANP without changing chemical processing behavior.
- Added `ChamanpConfig` as the first public runtime configuration object, with no chemical processing behavior changes.

## [v0.4.0] - 2026-05-13

- Added minimal package metadata in `pyproject.toml`.
- Added a minimal `chamanp` package namespace exposing `__version__`.
- Added package import smoke tests that do not run the pipeline or require source data.
- Documented the package transition direction and draft future public API.
- Changed project license metadata from MIT to `LGPL-3.0-or-later` by project-owner decision.
- No chemical curation, SMILES validation, collection filtering, fingerprint generation, reporting, or artifact naming changes are intended in this development pass.

## [v0.3.0] - 2026-05-13

- Added configuration preflight validation before pipeline execution.
- Added `ConfigurationError` for clear early failures when required config values are missing or invalid.
- Validated configured database and collection taxonomy paths before entering curation or fingerprint generation.
- Validated target collections, collection logic, safe collection tags, and Morgan fingerprint parameters.
- Hardened `TARGET_COLLECTIONS` validation to require a non-empty collection of non-empty strings.
- Added focused tests for preflight validation and entrypoint ordering.
- Removed unused `OUTPUT_PATH` from `config.py`.
- No chemical curation, SMILES validation, collection filtering, or fingerprint generation logic changes are intended in this development pass.

## [v0.2.0] - 2026-05-13

- Added centralized project metadata in `core/version.py`.
- Updated future report headers to use centralized CHAMANP version/status metadata.
- Added future report execution metadata for input CSV path, collection tag, fingerprint radius, fingerprint bit length, and valid fingerprinted molecule count.
- Removed the legacy hardcoded `v1.0 - May, 2025. Oviedo` report header for future reports.
- Added tests to ensure report headers include centralized metadata and do not contain the legacy `v1.0` version string.
- No chemical curation, collection filtering, or fingerprint generation logic changes are intended in this development pass.

## [v0.1.0] - 2026-05-13

- Added invalid SMILES traceability during fingerprint generation.
- Added `invalid_smiles_{tag}.csv` output through `PathManager` and `Pipeline`.
- Preserved existing valid fingerprint and valid metadata outputs.
- Replaced substring-based collection filtering with exact label matching.
- Collections are parsed as semicolon-separated labels with surrounding whitespace stripped.
- Missing/NaN collection values do not match.
- Added tests for substring non-match, semicolon-separated labels, whitespace handling, and missing/NaN values.
- Reports now include invalid SMILES count/path when provided by the pipeline.
- `FingerprintGenerator` exposes `invalid_smiles_count` for report traceability.
- `ReportWriter` remains backward-compatible when invalid fields are omitted.
- Added reporter tests and fingerprint count assertions.
- Updated tests; current validation is 29 tests passing.

## [dev-v1.0.1] - 2026-05-12

- CHAMANP is currently a pre-stable development prototype.
- This development pass prepares the project toward a corrected `v0.1.0`-style baseline by documenting the runtime environment, clarifying source-data expectations, and softening earlier stable-version language.
- Baseline tests were added for isolated non-RDKit components: `path_manager`, `collection_utils`, and `filter`.
- Baseline tests were added for isolated RDKit-related components: `curator` and `fingerprints`.
- Current validation is 21 tests passing.
- No pipeline behavior changes are intended in this baseline.
