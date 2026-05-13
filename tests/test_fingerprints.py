import numpy as np
import pandas as pd
import pytest

from core.fingerprints import FingerprintGenerator


def make_generator(tmp_path, rows=None, columns=None, output_invalid_file=None):
    input_csv = tmp_path / "filtered.csv"
    output_fp_file = tmp_path / "X_test.npy"
    output_metadata_file = tmp_path / "valid_metadata_test.csv"

    if columns is not None:
        pd.DataFrame(rows or [], columns=columns).to_csv(input_csv, index=False)
    elif rows is not None:
        pd.DataFrame(rows).to_csv(input_csv, index=False)

    return FingerprintGenerator(
        input_csv=input_csv,
        output_fp_file=output_fp_file,
        output_metadata_file=output_metadata_file,
        output_invalid_file=output_invalid_file,
    )


def test_get_morgan_fingerprint_returns_1024_length_integer_array(tmp_path):
    generator = make_generator(tmp_path)

    fingerprint = generator._get_morgan_fingerprint("CCO")

    assert isinstance(fingerprint, np.ndarray)
    assert fingerprint.shape == (1024,)
    assert np.issubdtype(fingerprint.dtype, np.integer)
    assert set(np.unique(fingerprint)).issubset({0, 1})


def test_get_morgan_fingerprint_returns_none_for_invalid_smiles(tmp_path):
    generator = make_generator(tmp_path)

    fingerprint = generator._get_morgan_fingerprint("not_a_smiles")

    assert fingerprint is None


def test_generate_writes_fingerprints_and_metadata_for_valid_rows_only(tmp_path):
    generator = make_generator(
        tmp_path,
        rows=[
            {"identifier": "id1", "canonical_smiles": "CCO", "name": "ethanol"},
            {
                "identifier": "id2",
                "canonical_smiles": "not_a_smiles",
                "name": "invalid",
            },
            {"identifier": "id3", "canonical_smiles": "CCN", "name": "ethylamine"},
        ],
    )

    result = generator.generate()

    assert result is generator
    assert generator.output_fp_file.exists()
    assert generator.output_metadata_file.exists()

    fingerprints = np.load(generator.output_fp_file)
    metadata = pd.read_csv(generator.output_metadata_file)

    assert fingerprints.shape == (2, 1024)
    assert metadata["identifier"].tolist() == ["id1", "id3"]
    assert generator.get_fingerprints().shape == (2, 1024)


def test_generate_skips_invalid_smiles(tmp_path):
    generator = make_generator(
        tmp_path,
        rows=[
            {"identifier": "id1", "canonical_smiles": "not_a_smiles"},
            {"identifier": "id2", "canonical_smiles": "CCC"},
        ],
    )

    generator.generate()

    metadata = pd.read_csv(generator.output_metadata_file)

    assert metadata["identifier"].tolist() == ["id2"]


def test_generate_writes_invalid_smiles_file_when_output_path_is_provided(tmp_path):
    output_invalid_file = tmp_path / "invalid_smiles_test.csv"
    generator = make_generator(
        tmp_path,
        output_invalid_file=output_invalid_file,
        rows=[
            {"identifier": "id1", "canonical_smiles": "CCO", "name": "ethanol"},
            {
                "identifier": "id2",
                "canonical_smiles": "not_a_smiles",
                "name": "invalid",
            },
            {"identifier": "id3", "canonical_smiles": "CCN", "name": "ethylamine"},
        ],
    )

    generator.generate()

    fingerprints = np.load(generator.output_fp_file)
    metadata = pd.read_csv(generator.output_metadata_file)
    invalid_metadata = pd.read_csv(output_invalid_file)

    assert fingerprints.shape == (2, 1024)
    assert metadata["identifier"].tolist() == ["id1", "id3"]
    assert output_invalid_file.exists()
    assert invalid_metadata["identifier"].tolist() == ["id2"]


def test_generate_writes_empty_invalid_smiles_file_when_no_invalid_rows(tmp_path):
    output_invalid_file = tmp_path / "invalid_smiles_test.csv"
    generator = make_generator(
        tmp_path,
        output_invalid_file=output_invalid_file,
        rows=[
            {"identifier": "id1", "canonical_smiles": "CCO", "name": "ethanol"},
            {"identifier": "id2", "canonical_smiles": "CCN", "name": "ethylamine"},
        ],
    )

    generator.generate()

    invalid_metadata = pd.read_csv(output_invalid_file)

    assert invalid_metadata.empty
    assert invalid_metadata.columns.tolist() == [
        "identifier",
        "canonical_smiles",
        "name",
    ]


def test_generate_raises_for_missing_smiles_column(tmp_path):
    generator = make_generator(
        tmp_path,
        rows=[{"identifier": "id1", "name": "ethanol"}],
    )

    with pytest.raises(KeyError, match="Column 'canonical_smiles' not found"):
        generator.generate()
