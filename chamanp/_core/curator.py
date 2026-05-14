# SPDX-License-Identifier: LGPL-3.0-or-later

# chamanp/_core/curator.py

import pandas as pd
from rdkit import Chem

class Curator:
    def __init__(self, input_csv, output_csv, smiles_column="canonical_smiles",
                 id_column="identifier", keep_columns=None, remove_stereo_duplicates=False):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.smiles_column = smiles_column
        self.id_column = id_column
        self.keep_columns = keep_columns
        self.remove_stereo_duplicates = remove_stereo_duplicates
        self.df = None

    def load_and_clean(self):
        try:
            self.df = pd.read_csv(self.input_csv, low_memory=False)
        except Exception as e:
            raise IOError(f"Error reading input CSV file: {e}")

        self.df = self.df[self.df[self.smiles_column].notna() & (self.df[self.smiles_column].str.strip() != "")]

        self.df = self.df.drop_duplicates(subset=[self.id_column, self.smiles_column])

        if self.remove_stereo_duplicates:
            self.df["smiles_nostereo"] = self.df[self.smiles_column].apply(self._canonicalize_smiles_nostereo)
            self.df = self.df.drop_duplicates(subset=["smiles_nostereo", "molecular_weight"])
            self.df.drop(columns=["smiles_nostereo"], inplace=True)

        if self.keep_columns:
            self.df = self.df[[c for c in self.keep_columns if c in self.df.columns]]

        self.df.to_csv(self.output_csv, index=False)
        return self

    def get_dataframe(self):
        return self.df.copy()

    def _canonicalize_smiles_nostereo(self, smiles):
        try:
            mol = Chem.MolFromSmiles(smiles)
            return Chem.MolToSmiles(mol, isomericSmiles=False)
        except Exception:
            return None
