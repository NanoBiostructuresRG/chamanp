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
    """Runtime configuration contract for a CHAMANP pipeline execution.

    All fields have defaults matching the current COCONUT reference molecular dataset
    configuration. Construct a custom configuration by passing field values
    directly, or load an external profile with ``from_module`` or
    ``from_toml``. Loaded configurations are not preflight-validated until
    ``validate_config`` is called.

    Attributes
    ----------
    DATABASE_PATH : str
        Path to the input molecular dataset CSV file.
        Default: ``"source_data/coconut_05-2025.csv"``.
    REPORTS_PATH : str
        Directory for pipeline execution reports.
        Default: ``"artifacts/reports"``.
    COLLECTION_TAXONOMY_PATH : str
        Path to the collection taxonomy JSON file.
        Default: ``"source_data/coconut_taxonomy.json"``.
    TARGET_COLLECTIONS : list of str
        Collection labels to include in the filtered dataset.
        Default: ``["PubChem NPs"]``.
    COLLECTION_TAG : str
        Short alphanumeric tag used in artifact file names.
        Default: ``"pubchem"``.
    COLLECTION_LOGIC : str
        Logical operator applied when filtering across target collections.
        Must be ``"OR"`` or ``"AND"``.
        Default: ``"OR"``.
    MORGAN_RADIUS : int
        Morgan fingerprint radius. Must be an integer >= 0.
        Default: ``2``.
    MORGAN_BITS : int
        Morgan fingerprint bit length. Must be a positive integer.
        Default: ``1024``.
    SELECTED_PROPERTIES : list of str
        Column names retained from the molecular dataset after curation.
        Default: the eight columns in ``DEFAULT_SELECTED_PROPERTIES``.
    REMOVE_STEREO_DUPLICATES : bool
        Whether stereochemical duplicates are removed during curation.
        Default: ``True``.

    Examples
    --------
    Construct a configuration with default values:

    >>> from chamanp import ChamanpConfig
    >>> config = ChamanpConfig()
    >>> config.COLLECTION_TAG
    'pubchem'

    Construct a configuration with custom values:

    >>> config = ChamanpConfig(
    ...     DATABASE_PATH="data/my_dataset.csv",
    ...     COLLECTION_TAXONOMY_PATH="data/taxonomy.json",
    ...     TARGET_COLLECTIONS=["Marine NPs"],
    ...     COLLECTION_TAG="marine",
    ...     COLLECTION_LOGIC="OR",
    ...     MORGAN_RADIUS=2,
    ...     MORGAN_BITS=2048,
    ... )
    >>> config.COLLECTION_TAG
    'marine'
    """

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
        """Build a ``ChamanpConfig`` from a module-like object.

        Reads every ``ChamanpConfig`` field name as an attribute from
        *module* and returns a new ``ChamanpConfig`` instance. The loaded
        configuration is not preflight-validated; call ``validate_config``
        to validate before execution.

        Parameters
        ----------
        module : module-like
            An object that exposes all ``ChamanpConfig`` field names as
            uppercase attributes, such as a Python module imported with
            ``import config``.

        Returns
        -------
        ChamanpConfig
            A new configuration instance populated from the module
            attributes.

        Raises
        ------
        AttributeError
            If any ``ChamanpConfig`` field name is absent from *module*.

        Examples
        --------
        Load configuration from the repository-level ``config.py``:

        >>> import config  # doctest: +SKIP
        >>> from chamanp import ChamanpConfig
        >>> cfg = ChamanpConfig.from_module(config)  # doctest: +SKIP
        """
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
        """Build a ``ChamanpConfig`` from a TOML file.

        Reads configuration values from a TOML file at *path*. TOML keys
        must be lowercase versions of ``ChamanpConfig`` field names (for
        example, ``database_path`` maps to ``DATABASE_PATH``). Unknown keys
        raise a ``ValueError``. The loaded configuration is not
        preflight-validated; call ``validate_config`` to validate before
        execution.

        Parameters
        ----------
        path : str or path-like
            File system path to the TOML configuration profile.

        Returns
        -------
        ChamanpConfig
            A new configuration instance populated from the TOML file.

        Raises
        ------
        FileNotFoundError
            If *path* does not exist.
        ValueError
            If the file is not valid TOML, or if it contains unknown keys.

        Notes
        -----
        ``from_toml`` does not perform preflight validation. File paths
        referenced in the loaded configuration are not checked for existence
        until ``validate_config`` is called.

        Examples
        --------
        Load configuration from the reference TOML profile:

        >>> from chamanp import ChamanpConfig
        >>> config = ChamanpConfig.from_toml("examples/chamanp.toml")  # doctest: +SKIP
        """
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
        """Return the names of all ``ChamanpConfig`` fields.

        Returns
        -------
        tuple of str
            Names of all configuration fields in declaration order.
        """
        return tuple(cls.__dataclass_fields__)

    @classmethod
    def _toml_field_map(cls):
        return {name.lower(): name for name in cls.required_fields()}


__all__ = ["ChamanpConfig", "DEFAULT_SELECTED_PROPERTIES"]
