from types import SimpleNamespace

import pytest

from core.preflight import ConfigurationError, validate_config


def make_config(tmp_path, **overrides):
    database_path = tmp_path / "input.csv"
    taxonomy_path = tmp_path / "taxonomy.json"
    database_path.write_text("identifier,canonical_smiles\n", encoding="utf-8")
    taxonomy_path.write_text('{"entries": ["PubChem NPs"]}', encoding="utf-8")

    values = {
        "DATABASE_PATH": str(database_path),
        "COLLECTION_TAXONOMY_PATH": str(taxonomy_path),
        "TARGET_COLLECTIONS": ["PubChem NPs"],
        "COLLECTION_LOGIC": " OR ",
        "COLLECTION_TAG": "pubchem_test-1",
        "MORGAN_RADIUS": 2,
        "MORGAN_BITS": 1024,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def assert_invalid(config, expected_message):
    with pytest.raises(ConfigurationError) as excinfo:
        validate_config(config)

    assert expected_message in str(excinfo.value)


def test_valid_config_passes_and_normalizes_harmless_whitespace(tmp_path):
    config = make_config(tmp_path)

    validated = validate_config(config)

    assert validated is config
    assert config.COLLECTION_LOGIC == "OR"
    assert config.COLLECTION_TAG == "pubchem_test-1"


def test_missing_database_path_fails(tmp_path):
    config = make_config(tmp_path, DATABASE_PATH=str(tmp_path / "missing.csv"))

    assert_invalid(config, "DATABASE_PATH does not exist")


def test_missing_collection_taxonomy_path_fails(tmp_path):
    config = make_config(
        tmp_path,
        COLLECTION_TAXONOMY_PATH=str(tmp_path / "missing_taxonomy.json"),
    )

    assert_invalid(config, "COLLECTION_TAXONOMY_PATH does not exist")


def test_empty_target_collections_fails(tmp_path):
    config = make_config(tmp_path, TARGET_COLLECTIONS=[])

    assert_invalid(config, "TARGET_COLLECTIONS is required and must not be empty")


def test_invalid_collection_logic_fails(tmp_path):
    config = make_config(tmp_path, COLLECTION_LOGIC="XOR")

    assert_invalid(config, "COLLECTION_LOGIC must be either 'OR' or 'AND'")


def test_empty_collection_tag_fails(tmp_path):
    config = make_config(tmp_path, COLLECTION_TAG=" ")

    assert_invalid(config, "COLLECTION_TAG is required and must not be empty")


def test_unsafe_collection_tag_fails(tmp_path):
    config = make_config(tmp_path, COLLECTION_TAG="../pubchem")

    assert_invalid(config, "COLLECTION_TAG may contain only")


def test_invalid_morgan_radius_fails(tmp_path):
    config = make_config(tmp_path, MORGAN_RADIUS=-1)

    assert_invalid(config, "MORGAN_RADIUS must be an integer >= 0")


def test_invalid_morgan_bits_fails(tmp_path):
    config = make_config(tmp_path, MORGAN_BITS=0)

    assert_invalid(config, "MORGAN_BITS must be a positive integer")
