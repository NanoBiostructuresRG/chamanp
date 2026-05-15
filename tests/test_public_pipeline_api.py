# SPDX-License-Identifier: LGPL-3.0-or-later
import os

import pytest

from chamanp import ChamanpConfig, ChamanpResult, run, validate_config


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


def test_public_run_returns_result_and_validates_before_execution(monkeypatch):
    calls = []
    config = ChamanpConfig(COLLECTION_TAG="pubchem")
    expected_result = ChamanpResult(
        status="completed",
        version="test",
        collection_tag="pubchem",
        curated_path="artifacts/curated_pubchem.csv",
        filtered_path="artifacts/filtered_pubchem.csv",
        metadata_path="artifacts/valid_metadata_pubchem.csv",
        fingerprints_path="artifacts/X_pubchem.npy",
        invalid_smiles_path="artifacts/invalid_smiles_pubchem.csv",
        report_path="artifacts/reports/report_dbprep_pubchem.txt",
        fingerprint_radius=2,
        fingerprint_bits=1024,
    )

    def fake_validate_config(active_config):
        calls.append(("validate", active_config))
        return active_config

    class FakePipeline:
        def __init__(self, config):
            calls.append(("pipeline_init", config))

        def run(self):
            calls.append(("pipeline_run", None))
            return expected_result

    import chamanp.pipeline as public_pipeline

    monkeypatch.setattr(public_pipeline, "_validate_config_impl", fake_validate_config)
    monkeypatch.setattr(public_pipeline, "_pipeline_cls", lambda: FakePipeline)

    result = run(config)

    assert result is expected_result
    assert calls == [
        ("validate", config),
        ("pipeline_init", config),
        ("pipeline_run", None),
    ]


def test_public_run_returns_result_and_writes_expected_artifacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    database_path = source_dir / "input.csv"
    taxonomy_path = source_dir / "taxonomy.json"
    database_path.write_text(
        "\n".join(
            [
                "identifier,canonical_smiles,molecular_weight,collections",
                "mol1,CCO,46.07,PubChem NPs",
                "mol2,not_a_smiles,100.00,PubChem NPs",
                "mol3,CCN,45.08,Other",
            ]
        ),
        encoding="utf-8",
    )
    taxonomy_path.write_text('{"entries": ["PubChem NPs", "Other"]}', encoding="utf-8")
    config = ChamanpConfig(
        DATABASE_PATH=str(database_path),
        REPORTS_PATH="artifacts/reports",
        COLLECTION_TAXONOMY_PATH=str(taxonomy_path),
        TARGET_COLLECTIONS=["PubChem NPs"],
        COLLECTION_TAG="pubchem_test",
        COLLECTION_LOGIC="OR",
        MORGAN_RADIUS=2,
        MORGAN_BITS=1024,
        SELECTED_PROPERTIES=[
            "identifier",
            "canonical_smiles",
            "molecular_weight",
            "collections",
        ],
        REMOVE_STEREO_DUPLICATES=True,
    )

    result = run(config)

    assert isinstance(result, ChamanpResult)
    assert result.status == "completed"
    assert result.collection_tag == "pubchem_test"
    assert result.fingerprint_radius == 2
    assert result.fingerprint_bits == 1024
    assert result.total_input_size == 3
    assert result.total_after_dedup == 3
    assert result.stereo_removed_count == 0
    assert result.filtered_count == 2
    assert result.valid_molecules_count == 1
    assert result.invalid_smiles_count == 1

    path_values = [
        result.curated_path,
        result.filtered_path,
        result.metadata_path,
        result.fingerprints_path,
        result.invalid_smiles_path,
        result.report_path,
    ]
    assert all(isinstance(path, str) for path in path_values)
    assert result.curated_path == "artifacts/curated_pubchem_test.csv"
    assert result.filtered_path == "artifacts/filtered_pubchem_test.csv"
    assert result.metadata_path == "artifacts/valid_metadata_pubchem_test.csv"
    assert result.fingerprints_path == "artifacts/X_pubchem_test.npy"
    assert result.invalid_smiles_path == "artifacts/invalid_smiles_pubchem_test.csv"
    assert result.report_path == "artifacts/reports/report_dbprep_pubchem_test.txt"
    assert result.to_dict()["collection_tag"] == "pubchem_test"

    for path in path_values:
        assert os.path.exists(path)


def test_public_run_raises_exception_without_failed_result(monkeypatch):
    config = ChamanpConfig(COLLECTION_TAG="pubchem")

    def fake_validate_config(active_config):
        return active_config

    class FailingPipeline:
        def __init__(self, config):
            self.config = config

        def run(self):
            raise RuntimeError("pipeline failed")

    import chamanp.pipeline as public_pipeline

    monkeypatch.setattr(public_pipeline, "_validate_config_impl", fake_validate_config)
    monkeypatch.setattr(public_pipeline, "_pipeline_cls", lambda: FailingPipeline)

    with pytest.raises(RuntimeError, match="pipeline failed"):
        run(config)
