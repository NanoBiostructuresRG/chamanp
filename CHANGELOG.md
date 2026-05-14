# Changelog

## [dev-v0.4.0] - Unreleased

- Added minimal package metadata in `pyproject.toml`.
- Added a minimal `chamanp` package namespace exposing `__version__`.
- Added package import smoke tests that do not run the pipeline or require source data.
- Documented the package transition direction and draft future public API.
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
