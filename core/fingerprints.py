
# core/fingerprints.py

import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

class FingerprintGenerator:
    def __init__(self, input_csv, output_fp_file, output_metadata_file, smiles_column="canonical_smiles"):
        self.input_csv = input_csv
        self.output_fp_file = output_fp_file
        self.output_metadata_file = output_metadata_file
        self.smiles_column = smiles_column
        self.morgan_generator = GetMorganGenerator(radius=2, fpSize=1024)
        self.X = None

    def _get_morgan_fingerprint(self, smiles):
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                fp = self.morgan_generator.GetFingerprint(mol)
                return np.array([int(bit) for bit in fp.ToBitString()], dtype=int)
        except Exception:
            return None
        return None

    def generate(self):
        try:
            df = pd.read_csv(self.input_csv)
        except Exception as e:
            raise IOError(f"Failed to read input CSV file: {e}")

        if self.smiles_column not in df.columns:
            raise KeyError(f"Column '{self.smiles_column}' not found in input data.")

        fingerprints = []
        valid_rows = []

        for _, row in df.iterrows():
            fp = self._get_morgan_fingerprint(row[self.smiles_column])
            if fp is not None:
                fingerprints.append(fp)
                valid_rows.append(row)

        self.X = np.array(fingerprints, dtype=int)

        try:
            pd.DataFrame(valid_rows).to_csv(self.output_metadata_file, index=False)
            np.save(self.output_fp_file, self.X)
        except Exception as e:
            raise IOError(f"Failed to save fingerprints or metadata: {e}")

        return self

    def get_fingerprints(self):
        return self.X.copy() if self.X is not None else None
