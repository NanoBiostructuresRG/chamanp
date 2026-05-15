# SPDX-License-Identifier: LGPL-3.0-or-later
"""Public runtime configuration contract for CHAMANP."""

from dataclasses import MISSING, dataclass, field, fields
from pathlib import Path
import tomllib


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
    def from_toml(cls, path):
        """Build a configuration object from a TOML file."""
        config_path = Path(path)

        try:
            with config_path.open("rb") as config_file:
                loaded = tomllib.load(config_file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"TOML configuration file not found: {config_path}"
            ) from exc
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"Malformed TOML configuration file: {config_path}: {exc}") from exc

        field_map = cls._toml_field_map()
        values = {}

        for key, value in loaded.items():
            if key not in field_map:
                raise ValueError(f"Unknown configuration field: {key}")
            values[field_map[key]] = value

        missing = [
            field.name.lower()
            for field in fields(cls)
            if field.name not in values
            and field.default is MISSING
            and field.default_factory is MISSING
        ]
        if missing:
            missing_fields = ", ".join(missing)
            raise ValueError(f"Missing required configuration field(s): {missing_fields}")

        return cls(**values)

    @classmethod
    def required_fields(cls):
        """Return the attribute names required by the current pipeline."""
        return tuple(cls.__dataclass_fields__)

    @classmethod
    def _toml_field_map(cls):
        return {name.lower(): name for name in cls.required_fields()}


__all__ = ["ChamanpConfig", "DEFAULT_SELECTED_PROPERTIES"]
