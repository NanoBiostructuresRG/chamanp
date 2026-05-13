# Changelog

## [dev-v0.1.0] - 2026-05-13

- Added invalid SMILES traceability during fingerprint generation.
- Added `invalid_smiles_{tag}.csv` output through `PathManager` and `Pipeline`.
- Preserved existing valid fingerprint and valid metadata outputs.
- Updated tests; current validation is 23 tests passing.

## [dev-v1.0.1] - 2026-05-12

- CHAMANP is currently a pre-stable development prototype.
- This development pass prepares the project toward a corrected `v0.1.0`-style baseline by documenting the runtime environment, clarifying source-data expectations, and softening earlier stable-version language.
- Baseline tests were added for isolated non-RDKit components: `path_manager`, `collection_utils`, and `filter`.
- Baseline tests were added for isolated RDKit-related components: `curator` and `fingerprints`.
- Current validation is 21 tests passing.
- No pipeline behavior changes are intended in this baseline.
