# SPDX-License-Identifier: LGPL-3.0-or-later
from chamanp import ChamanpConfig, run, validate_config


def make_valid_config(tmp_path):
    database_path = tmp_path / "input.csv"
    taxonomy_path = tmp_path / "taxonomy.json"
    database_path.write_text("identifier,canonical_smiles\n", encoding="utf-8")
    taxonomy_path.write_text('{"entries": ["PubChem NPs"]}', encoding="utf-8")

    return ChamanpConfig(
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


def test_public_validate_config_returns_validated_chamanp_config(tmp_path):
    config = make_valid_config(tmp_path)

    validated = validate_config(config)

    assert validated is config
    assert validated.COLLECTION_LOGIC == "AND"
    assert validated.COLLECTION_TAG == "pubchem_test"


def test_public_run_returns_none_and_validates_before_execution(monkeypatch):
    calls = []
    config = ChamanpConfig(COLLECTION_TAG="pubchem")

    def fake_validate_config(active_config):
        calls.append(("validate", active_config))
        return active_config

    class FakePipeline:
        def __init__(self, config):
            calls.append(("pipeline_init", config))

        def run(self):
            calls.append(("pipeline_run", None))

    import chamanp.pipeline as public_pipeline

    monkeypatch.setattr(public_pipeline, "_validate_config_impl", fake_validate_config)
    monkeypatch.setattr(public_pipeline, "_pipeline_cls", lambda: FakePipeline)

    result = run(config)

    assert result is None
    assert calls == [
        ("validate", config),
        ("pipeline_init", config),
        ("pipeline_run", None),
    ]
