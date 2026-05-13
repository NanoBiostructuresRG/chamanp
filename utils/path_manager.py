
# utils/path_manager.py

class PathManager:
    def __init__(self, tag: str, base_dir: str = "artifacts"):
        self.tag = tag
        self.base_dir = base_dir

    def curated(self):
        return f"{self.base_dir}/curated_{self.tag}.csv"

    def filtered(self):
        return f"{self.base_dir}/filtered_{self.tag}.csv"

    def metadata(self):
        return f"{self.base_dir}/valid_metadata_{self.tag}.csv"

    def fingerprints(self):
        return f"{self.base_dir}/X_{self.tag}.npy"

    def invalid_smiles(self):
        return f"{self.base_dir}/invalid_smiles_{self.tag}.csv"
