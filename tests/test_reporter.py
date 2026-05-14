# SPDX-License-Identifier: LGPL-3.0-or-later
from pathlib import Path
from types import SimpleNamespace

from core.reporter import ReportWriter
from core.fingerprints import MORGAN_BITS, MORGAN_RADIUS
from core.version import PROJECT_NAME, PROJECT_STATUS, PROJECT_VERSION


def build_report(**overrides):
    writer = ReportWriter(config=SimpleNamespace(REPORTS_PATH="unused"))
    values = {
        "total_input_size": 10,
        "total_after_dedup": 8,
        "stereo_removed_count": 2,
        "target_collections": ["PubChem NPs"],
        "logic": "OR",
        "final_count": 3,
        "retained_properties": ["identifier", "canonical_smiles"],
        "curated_csv": "artifacts/curated_pubchem.csv",
        "filtered_csv": "artifacts/filtered_pubchem.csv",
        "metadata_csv": "artifacts/valid_metadata_pubchem.csv",
        "fingerprints_npy": "artifacts/X_pubchem.npy",
        "collection_tag": "pubchem",
        "input_csv": "source_data/coconut_05-2025.csv",
        "fingerprint_radius": MORGAN_RADIUS,
        "fingerprint_bits": MORGAN_BITS,
        "valid_molecules_count": 2,
    }
    values.update(overrides)
    return writer._build_content(**values)


def test_build_content_includes_invalid_smiles_traceability():
    content = build_report(
        invalid_smiles_csv="artifacts/invalid_smiles_pubchem.csv",
        invalid_smiles_count=1,
    )

    assert "Invalid SMILES rows:          1" in content
    assert "- Invalid SMILES CSV: artifacts/invalid_smiles_pubchem.csv" in content
    assert "- Metadata CSV:      artifacts/valid_metadata_pubchem.csv" in content
    assert "- Fingerprints NPY:  artifacts/X_pubchem.npy" in content


def test_build_content_includes_execution_metadata():
    content = build_report(
        invalid_smiles_csv="artifacts/invalid_smiles_pubchem.csv",
        invalid_smiles_count=1,
    )

    assert "Execution metadata:" in content
    assert "- Collection tag:    pubchem" in content
    assert "- Input CSV:         source_data/coconut_05-2025.csv" in content
    assert f"- Fingerprint radius: {MORGAN_RADIUS}" in content
    assert f"- Fingerprint bits:   {MORGAN_BITS}" in content
    assert "Valid molecules fingerprinted: 2" in content


def test_build_content_remains_compatible_without_invalid_smiles_fields():
    content = build_report()

    assert "Invalid SMILES rows:" not in content
    assert "Invalid SMILES CSV:" not in content
    assert "- Metadata CSV:      artifacts/valid_metadata_pubchem.csv" in content
    assert "- Fingerprints NPY:  artifacts/X_pubchem.npy" in content


def test_generate_phase2_report_writes_report_with_project_metadata(tmp_path):
    writer = ReportWriter(config=SimpleNamespace(REPORTS_PATH=str(tmp_path)))

    report_path = writer.generate_phase2_report(
        total_input_size=10,
        total_after_dedup=8,
        stereo_removed_count=2,
        target_collections=["PubChem NPs"],
        logic="OR",
        final_count=3,
        retained_properties=["identifier", "canonical_smiles"],
        curated_csv="artifacts/curated_pubchem.csv",
        filtered_csv="artifacts/filtered_pubchem.csv",
        metadata_csv="artifacts/valid_metadata_pubchem.csv",
        fingerprints_npy="artifacts/X_pubchem.npy",
        collection_tag="pubchem",
        invalid_smiles_csv="artifacts/invalid_smiles_pubchem.csv",
        invalid_smiles_count=1,
        input_csv="source_data/coconut_05-2025.csv",
        valid_molecules_count=2,
        fingerprint_radius=MORGAN_RADIUS,
        fingerprint_bits=MORGAN_BITS,
    )

    report_file = tmp_path / "report_dbprep_pubchem.txt"
    content = report_file.read_text(encoding="utf-8")

    assert Path(report_path) == report_file
    assert report_file.exists()
    assert PROJECT_NAME in content
    assert f"Version: {PROJECT_VERSION}" in content
    assert f"Status: {PROJECT_STATUS}" in content
    assert "Execution Date:" in content
    assert "Invalid SMILES rows:          1" in content
    assert "- Invalid SMILES CSV: artifacts/invalid_smiles_pubchem.csv" in content
