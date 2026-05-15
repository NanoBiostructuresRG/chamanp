# SPDX-License-Identifier: LGPL-3.0-or-later
from dataclasses import MISSING
from types import SimpleNamespace

import pytest

from chamanp import ChamanpConfig, __version__
from chamanp.config import DEFAULT_SELECTED_PROPERTIES
from chamanp._core.preflight import validate_config


def make_module_like_config(**overrides):
    values = {
        "DATABASE_PATH": "input.csv",
        "REPORTS_PATH": "artifacts/reports",
        "COLLECTION_TAXONOMY_PATH": "taxonomy.json",
        "TARGET_COLLECTIONS": ["PubChem NPs"],
        "COLLECTION_TAG": "pubchem",
        "COLLECTION_LOGIC": "OR",
        "MORGAN_RADIUS": 2,
        "MORGAN_BITS": 1024,
        "SELECTED_PROPERTIES": ["identifier", "canonical_smiles", "collections"],
        "REMOVE_STEREO_DUPLICATES": True,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_chamanp_config_is_publicly_importable():
    assert ChamanpConfig.__name__ == "ChamanpConfig"
    assert isinstance(__version__, str)


def test_chamanp_config_can_be_instantiated_manually():
    config = ChamanpConfig(
        DATABASE_PATH="input.csv",
        REPORTS_PATH="reports",
        COLLECTION_TAXONOMY_PATH="taxonomy.json",
        TARGET_COLLECTIONS=["PubChem NPs"],
        COLLECTION_TAG="pubchem",
        COLLECTION_LOGIC="OR",
        MORGAN_RADIUS=2,
        MORGAN_BITS=1024,
        SELECTED_PROPERTIES=["identifier", "canonical_smiles"],
        REMOVE_STEREO_DUPLICATES=True,
    )

    assert config.DATABASE_PATH == "input.csv"
    assert config.TARGET_COLLECTIONS == ["PubChem NPs"]
    assert config.MORGAN_RADIUS == 2


def test_chamanp_config_from_module_reads_required_attributes():
    module_config = make_module_like_config(COLLECTION_TAG="pubchem_test")

    config = ChamanpConfig.from_module(module_config)

    assert config.DATABASE_PATH == module_config.DATABASE_PATH
    assert config.REPORTS_PATH == module_config.REPORTS_PATH
    assert config.COLLECTION_TAG == "pubchem_test"
    assert config.SELECTED_PROPERTIES == module_config.SELECTED_PROPERTIES


def test_chamanp_config_from_module_fails_for_missing_required_attribute():
    module_config = make_module_like_config()
    del module_config.MORGAN_BITS

    with pytest.raises(AttributeError, match="MORGAN_BITS"):
        ChamanpConfig.from_module(module_config)


def test_chamanp_config_from_toml_loads_valid_minimal_profile(tmp_path):
    profile_path = tmp_path / "chamanp.toml"
    profile_path.write_text(
        "\n".join(
            [
                'database_path = "input.csv"',
                'collection_taxonomy_path = "taxonomy.json"',
                'target_collections = ["PubChem NPs"]',
                'collection_tag = "pubchem_test"',
                'collection_logic = "OR"',
            ]
        ),
        encoding="utf-8",
    )

    config = ChamanpConfig.from_toml(profile_path)

    assert config.DATABASE_PATH == "input.csv"
    assert config.COLLECTION_TAXONOMY_PATH == "taxonomy.json"
    assert config.TARGET_COLLECTIONS == ["PubChem NPs"]
    assert config.COLLECTION_TAG == "pubchem_test"
    assert config.COLLECTION_LOGIC == "OR"


def test_chamanp_config_from_toml_accepts_string_path(tmp_path):
    profile_path = tmp_path / "chamanp.toml"
    profile_path.write_text('collection_tag = "from_string"\n', encoding="utf-8")

    config = ChamanpConfig.from_toml(str(profile_path))

    assert config.COLLECTION_TAG == "from_string"


def test_chamanp_config_from_toml_fails_for_missing_file(tmp_path):
    profile_path = tmp_path / "missing.toml"

    with pytest.raises(FileNotFoundError, match="TOML configuration file not found"):
        ChamanpConfig.from_toml(profile_path)


def test_chamanp_config_from_toml_fails_for_malformed_toml(tmp_path):
    profile_path = tmp_path / "chamanp.toml"
    profile_path.write_text("collection_tag = [\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed TOML configuration file"):
        ChamanpConfig.from_toml(profile_path)


def test_chamanp_config_from_toml_fails_for_unknown_field(tmp_path):
    profile_path = tmp_path / "chamanp.toml"
    profile_path.write_text('morgan_radios = 2\n', encoding="utf-8")

    with pytest.raises(ValueError, match="Unknown configuration field: morgan_radios"):
        ChamanpConfig.from_toml(profile_path)


def test_chamanp_config_from_toml_preserves_defaults_for_omitted_fields(tmp_path):
    profile_path = tmp_path / "chamanp.toml"
    profile_path.write_text('collection_tag = "defaults"\n', encoding="utf-8")

    config = ChamanpConfig.from_toml(profile_path)

    assert config.COLLECTION_TAG == "defaults"
    assert config.DATABASE_PATH == "source_data/coconut_05-2025.csv"
    assert config.REPORTS_PATH == "artifacts/reports"
    assert config.MORGAN_RADIUS == 2
    assert config.MORGAN_BITS == 1024
    assert config.SELECTED_PROPERTIES == DEFAULT_SELECTED_PROPERTIES
    assert config.REMOVE_STEREO_DUPLICATES is True


def test_chamanp_config_from_toml_has_no_current_missing_required_fields():
    required_without_defaults = [
        name
        for name, field in ChamanpConfig.__dataclass_fields__.items()
        if field.default is MISSING and field.default_factory is MISSING
    ]

    assert required_without_defaults == []


def test_importing_chamanp_with_config_export_has_no_pipeline_side_effects(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    import chamanp

    assert chamanp.ChamanpConfig is ChamanpConfig
    assert not (tmp_path / "artifacts").exists()
    assert not (tmp_path / "artifacts" / "pipeline.log").exists()


def test_validate_config_accepts_chamanp_config_without_preflight_changes(tmp_path):
    database_path = tmp_path / "input.csv"
    taxonomy_path = tmp_path / "taxonomy.json"
    database_path.write_text("identifier,canonical_smiles\n", encoding="utf-8")
    taxonomy_path.write_text('{"entries": ["PubChem NPs"]}', encoding="utf-8")
    config = ChamanpConfig(
        DATABASE_PATH=str(database_path),
        REPORTS_PATH=str(tmp_path / "reports"),
        COLLECTION_TAXONOMY_PATH=str(taxonomy_path),
        TARGET_COLLECTIONS=["PubChem NPs"],
        COLLECTION_TAG=" pubchem_test ",
        COLLECTION_LOGIC=" and ",
        MORGAN_RADIUS=2,
        MORGAN_BITS=1024,
        SELECTED_PROPERTIES=["identifier", "canonical_smiles"],
        REMOVE_STEREO_DUPLICATES=True,
    )

    validated = validate_config(config)

    assert validated is config
    assert config.COLLECTION_LOGIC == "AND"
    assert config.COLLECTION_TAG == "pubchem_test"


def test_validate_config_accepts_chamanp_config_loaded_from_toml(tmp_path):
    database_path = tmp_path / "input.csv"
    taxonomy_path = tmp_path / "taxonomy.json"
    profile_path = tmp_path / "chamanp.toml"
    database_path.write_text("identifier,canonical_smiles\n", encoding="utf-8")
    taxonomy_path.write_text('{"entries": ["PubChem NPs"]}', encoding="utf-8")
    profile_path.write_text(
        "\n".join(
            [
                f'database_path = "{database_path.as_posix()}"',
                f'collection_taxonomy_path = "{taxonomy_path.as_posix()}"',
                'target_collections = ["PubChem NPs"]',
                'collection_tag = " toml_test "',
                'collection_logic = " and "',
                "morgan_radius = 2",
                "morgan_bits = 1024",
            ]
        ),
        encoding="utf-8",
    )

    config = ChamanpConfig.from_toml(profile_path)
    validated = validate_config(config)

    assert validated is config
    assert config.COLLECTION_TAG == "toml_test"
    assert config.COLLECTION_LOGIC == "AND"
