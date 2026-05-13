import pandas as pd

from core.curator import Curator


def write_compounds(path, rows):
    pd.DataFrame(rows).to_csv(path, index=False)


def run_curator(tmp_path, rows, keep_columns=None, remove_stereo_duplicates=False):
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "curated.csv"
    write_compounds(input_csv, rows)

    return Curator(
        input_csv=input_csv,
        output_csv=output_csv,
        keep_columns=keep_columns,
        remove_stereo_duplicates=remove_stereo_duplicates,
    ).load_and_clean()


def test_load_and_clean_removes_missing_or_blank_smiles_rows(tmp_path):
    curator = run_curator(
        tmp_path=tmp_path,
        rows=[
            {"identifier": "id1", "canonical_smiles": "CCO", "molecular_weight": 46.07},
            {"identifier": "id2", "canonical_smiles": "", "molecular_weight": 0.0},
            {"identifier": "id3", "canonical_smiles": None, "molecular_weight": 0.0},
            {"identifier": "id4", "canonical_smiles": "   ", "molecular_weight": 0.0},
        ],
    )

    curated = curator.get_dataframe()

    assert curated["identifier"].tolist() == ["id1"]


def test_load_and_clean_removes_exact_duplicate_identifier_smiles_rows(tmp_path):
    curator = run_curator(
        tmp_path=tmp_path,
        rows=[
            {"identifier": "id1", "canonical_smiles": "CCO", "molecular_weight": 46.07},
            {"identifier": "id1", "canonical_smiles": "CCO", "molecular_weight": 46.07},
            {"identifier": "id2", "canonical_smiles": "CCO", "molecular_weight": 46.07},
        ],
    )

    curated = curator.get_dataframe()

    assert curated["identifier"].tolist() == ["id1", "id2"]


def test_load_and_clean_keeps_existing_requested_columns_and_ignores_missing(tmp_path):
    curator = run_curator(
        tmp_path=tmp_path,
        rows=[
            {
                "identifier": "id1",
                "canonical_smiles": "CCO",
                "name": "ethanol",
                "molecular_weight": 46.07,
            }
        ],
        keep_columns=["identifier", "missing_column", "canonical_smiles"],
    )

    curated = curator.get_dataframe()

    assert curated.columns.tolist() == ["identifier", "canonical_smiles"]


def test_load_and_clean_removes_stereo_duplicates_when_enabled(tmp_path):
    curator = run_curator(
        tmp_path=tmp_path,
        rows=[
            {
                "identifier": "id1",
                "canonical_smiles": "C[C@H](O)Cl",
                "molecular_weight": 80.51,
            },
            {
                "identifier": "id2",
                "canonical_smiles": "CC(O)Cl",
                "molecular_weight": 80.51,
            },
            {
                "identifier": "id3",
                "canonical_smiles": "CCN",
                "molecular_weight": 45.08,
            },
        ],
        remove_stereo_duplicates=True,
    )

    curated = curator.get_dataframe()

    assert curated["identifier"].tolist() == ["id1", "id3"]


def test_get_dataframe_returns_copy(tmp_path):
    curator = run_curator(
        tmp_path=tmp_path,
        rows=[
            {"identifier": "id1", "canonical_smiles": "CCO", "molecular_weight": 46.07}
        ],
    )

    first_copy = curator.get_dataframe()
    first_copy.loc[first_copy.index[0], "identifier"] = "mutated"

    second_copy = curator.get_dataframe()

    assert second_copy["identifier"].tolist() == ["id1"]
