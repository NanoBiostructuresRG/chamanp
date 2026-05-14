# SPDX-License-Identifier: LGPL-3.0-or-later
import json

import pytest

from chamanp._utils.collection_utils import CollectionValidator


def write_taxonomy(path, entries):
    path.write_text(json.dumps({"entries": entries}), encoding="utf-8")


def test_validate_returns_known_and_unknown_collections_sorted(tmp_path):
    taxonomy_path = tmp_path / "taxonomy.json"
    write_taxonomy(taxonomy_path, ["PubChem NPs", "ChEMBL NPs", "FooDB"])

    validator = CollectionValidator(taxonomy_json_path=taxonomy_path)
    known, unknown = validator.validate(["Unknown DB", "FooDB", "PubChem NPs"])

    assert known == ["FooDB", "PubChem NPs"]
    assert unknown == ["Unknown DB"]


def test_validate_with_real_taxonomy_accepts_pubchem_nps():
    validator = CollectionValidator(
        taxonomy_json_path="source_data/coconut_taxonomy.json"
    )

    known, unknown = validator.validate(["PubChem NPs"])

    assert known == ["PubChem NPs"]
    assert unknown == []


def test_missing_taxonomy_file_raises_file_not_found(tmp_path):
    missing_path = tmp_path / "missing_taxonomy.json"

    with pytest.raises(FileNotFoundError, match="Taxonomy file not found"):
        CollectionValidator(taxonomy_json_path=missing_path)


def test_invalid_taxonomy_json_raises_value_error(tmp_path):
    taxonomy_path = tmp_path / "invalid_taxonomy.json"
    taxonomy_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON format"):
        CollectionValidator(taxonomy_json_path=taxonomy_path)
