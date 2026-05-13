from utils.path_manager import PathManager


def test_path_manager_builds_expected_artifact_paths_for_tag():
    paths = PathManager(tag="pubchem")

    assert paths.curated() == "artifacts/curated_pubchem.csv"
    assert paths.filtered() == "artifacts/filtered_pubchem.csv"
    assert paths.metadata() == "artifacts/valid_metadata_pubchem.csv"
    assert paths.fingerprints() == "artifacts/X_pubchem.npy"
    assert paths.invalid_smiles() == "artifacts/invalid_smiles_pubchem.csv"


def test_path_manager_respects_custom_base_dir():
    paths = PathManager(tag="pubchem", base_dir="tmp_outputs")

    assert paths.curated() == "tmp_outputs/curated_pubchem.csv"
    assert paths.filtered() == "tmp_outputs/filtered_pubchem.csv"
    assert paths.metadata() == "tmp_outputs/valid_metadata_pubchem.csv"
    assert paths.fingerprints() == "tmp_outputs/X_pubchem.npy"
    assert paths.invalid_smiles() == "tmp_outputs/invalid_smiles_pubchem.csv"
