# SPDX-License-Identifier: LGPL-3.0-or-later
from types import SimpleNamespace

import pytest

from chamanp import ChamanpConfig, __version__
from core.preflight import validate_config


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
