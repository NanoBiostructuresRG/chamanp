# SPDX-License-Identifier: LGPL-3.0-or-later
"""Public runtime configuration contract for CHAMANP."""

from dataclasses import dataclass, field


DEFAULT_SELECTED_PROPERTIES = [
    "identifier",
    "canonical_smiles",
    "name",
    "molecular_weight",
    "alogp",
    "topological_polar_surface_area",
    "np_likeness",
    "collections",
]


@dataclass
class ChamanpConfig:
    """Runtime configuration object compatible with the current pipeline."""

    DATABASE_PATH: str = "source_data/coconut_05-2025.csv"
    REPORTS_PATH: str = "artifacts/reports"
    COLLECTION_TAXONOMY_PATH: str = "source_data/coconut_taxonomy.json"
    TARGET_COLLECTIONS: list[str] = field(default_factory=lambda: ["PubChem NPs"])
    COLLECTION_TAG: str = "pubchem"
    COLLECTION_LOGIC: str = "OR"
    MORGAN_RADIUS: int = 2
    MORGAN_BITS: int = 1024
    SELECTED_PROPERTIES: list[str] = field(
        default_factory=lambda: list(DEFAULT_SELECTED_PROPERTIES)
    )
    REMOVE_STEREO_DUPLICATES: bool = True

    @classmethod
    def from_module(cls, module):
        """Build a configuration object from a module-like object."""
        values = {}
        missing = []

        for name in cls.required_fields():
            if hasattr(module, name):
                values[name] = getattr(module, name)
            else:
                missing.append(name)

        if missing:
            missing_fields = ", ".join(missing)
            raise AttributeError(
                f"Missing required CHAMANP configuration attribute(s): {missing_fields}"
            )

        return cls(**values)

    @classmethod
    def required_fields(cls):
        """Return the attribute names required by the current pipeline."""
        return tuple(cls.__dataclass_fields__)


__all__ = ["ChamanpConfig", "DEFAULT_SELECTED_PROPERTIES"]
