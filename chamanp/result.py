# SPDX-License-Identifier: LGPL-3.0-or-later
"""Public execution result contract for CHAMANP."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ChamanpResult:
    """Frozen summary of a completed CHAMANP pipeline execution.

    Returned by ``run`` after a successful pipeline run. All path fields
    are strings. Count fields may be ``None`` if the pipeline did not
    produce them. Execution failures are exception-based and do not
    produce a result object.

    Notes
    -----
    CHAMANP is currently pre-stable (Alpha). Field names and types may
    change before a stable release is declared.

    Attributes
    ----------
    status : str
        Execution status. Always ``"completed"`` for a successful run.
    version : str
        CHAMANP package version at the time of execution.
    collection_tag : str
        Short collection tag used to name output artifacts, taken from
        ``ChamanpConfig.COLLECTION_TAG``.
    curated_path : str
        File system path to the curated molecular dataset CSV.
    filtered_path : str
        File system path to the collection-filtered dataset CSV.
    metadata_path : str
        File system path to the fingerprint metadata CSV.
    fingerprints_path : str
        File system path to the Morgan fingerprint matrix (``.npy``).
    invalid_smiles_path : str
        File system path to the invalid-SMILES traceability CSV.
    report_path : str
        File system path to the pipeline execution report.
    fingerprint_radius : int
        Morgan fingerprint radius used during generation, taken from
        ``ChamanpConfig.MORGAN_RADIUS``.
    fingerprint_bits : int
        Morgan fingerprint bit length used during generation, taken from
        ``ChamanpConfig.MORGAN_BITS``.
    total_input_size : int or None
        Total number of data rows in the input CSV, excluding the header.
    total_after_dedup : int or None
        Number of rows remaining after stereochemical deduplication.
    stereo_removed_count : int or None
        Number of rows removed during stereochemical deduplication
        (``total_input_size - total_after_dedup``).
    filtered_count : int or None
        Number of molecular dataset entries remaining after collection filtering.
    valid_molecules_count : int or None
        Number of molecular dataset entries for which a valid fingerprint was generated.
        (``filtered_count - invalid_smiles_count``).
    invalid_smiles_count : int or None
        Number of compounds whose SMILES string could not be parsed by
        RDKit during fingerprint generation.
    """

    status: str
    version: str
    collection_tag: str
    curated_path: str
    filtered_path: str
    metadata_path: str
    fingerprints_path: str
    invalid_smiles_path: str
    report_path: str
    fingerprint_radius: int
    fingerprint_bits: int
    total_input_size: int | None = None
    total_after_dedup: int | None = None
    stereo_removed_count: int | None = None
    filtered_count: int | None = None
    valid_molecules_count: int | None = None
    invalid_smiles_count: int | None = None

    def to_dict(self):
        """Return a plain-dictionary representation of the execution result.

        Returns
        -------
        dict
            A dictionary with field names as keys and field values as
            values, produced by ``dataclasses.asdict``.
        """
        return asdict(self)


__all__ = ["ChamanpResult"]
