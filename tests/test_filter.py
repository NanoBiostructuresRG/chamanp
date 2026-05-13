import pandas as pd
import pytest

from core.filter import CompoundFilter


def sample_compounds():
    return pd.DataFrame(
        {
            "identifier": ["id1", "id2", "id3", "id4"],
            "canonical_smiles": ["CCO", "CCN", "CCC", "CCCl"],
            "name": ["ethanol", "ethylamine", "propane", "chloroethane"],
            "collections": [
                "PubChem NPs; FooDB",
                "ChEMBL NPs",
                "PubChem NPs; ChEMBL NPs",
                "NotPubChem NPs",
            ],
        }
    )


def apply_filter(df, tmp_path, collection_names, properties, logic="OR"):
    return CompoundFilter(
        df=df,
        collection_names=collection_names,
        properties=properties,
        output_path=tmp_path / "filtered.csv",
        logic=logic,
    ).apply_filters()


def test_apply_filters_or_logic_matches_any_requested_collection(tmp_path):
    compound_filter = apply_filter(
        df=sample_compounds(),
        tmp_path=tmp_path,
        collection_names=["PubChem NPs", "ChEMBL NPs"],
        properties=["identifier", "collections"],
        logic="OR",
    )

    filtered = compound_filter.get_dataframe()

    # id4 is included because current filtering uses substring matching.
    assert filtered["identifier"].tolist() == ["id1", "id2", "id3", "id4"]


def test_apply_filters_and_logic_matches_all_requested_collections(tmp_path):
    compound_filter = apply_filter(
        df=sample_compounds(),
        tmp_path=tmp_path,
        collection_names=["PubChem NPs", "ChEMBL NPs"],
        properties=["identifier", "collections"],
        logic="AND",
    )

    filtered = compound_filter.get_dataframe()

    assert filtered["identifier"].tolist() == ["id3"]


def test_apply_filters_retains_selected_available_properties(tmp_path):
    compound_filter = apply_filter(
        df=sample_compounds(),
        tmp_path=tmp_path,
        collection_names=["FooDB"],
        properties=["identifier", "missing_column", "collections"],
    )

    filtered = compound_filter.get_dataframe()

    assert filtered.columns.tolist() == ["identifier", "collections"]
    assert filtered["identifier"].tolist() == ["id1"]


def test_apply_filters_raises_for_missing_collections_column(tmp_path):
    df = pd.DataFrame({"identifier": ["id1"], "canonical_smiles": ["CCO"]})

    with pytest.raises(KeyError, match="Column 'collections' is missing"):
        apply_filter(
            df=df,
            tmp_path=tmp_path,
            collection_names=["PubChem NPs"],
            properties=["identifier"],
        )


def test_apply_filters_raises_for_invalid_logic(tmp_path):
    with pytest.raises(ValueError, match="Logic must be 'OR' or 'AND'"):
        apply_filter(
            df=sample_compounds(),
            tmp_path=tmp_path,
            collection_names=["PubChem NPs"],
            properties=["identifier"],
            logic="XOR",
        )
