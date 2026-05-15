# SPDX-License-Identifier: LGPL-3.0-or-later
"""Public execution result contract for CHAMANP."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ChamanpResult:
    """Lightweight summary of a CHAMANP execution."""

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
        """Return a dictionary representation of the execution result."""
        return asdict(self)


__all__ = ["ChamanpResult"]
