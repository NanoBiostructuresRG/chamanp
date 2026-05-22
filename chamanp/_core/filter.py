# SPDX-License-Identifier: LGPL-3.0-or-later

# chamanp/_core/filter.py

import re

import pandas as pd

class CompoundFilter:
    def __init__(self, df, collection_names, properties, output_path, logic="OR"):
        self.df = df
        self.collection_names = collection_names
        self.properties = properties
        self.output_path = output_path
        self.logic = logic.upper()
        self.filtered_df = None

    def apply_filters(self):
        if "collections" not in self.df.columns:
            raise KeyError("Column 'collections' is missing from input DataFrame.")

        if self.logic == "OR":
            mask = self.df["collections"].apply(
                lambda x: any(
                    c in self._parse_collections(x)
                    for c in self.collection_names
                )
            )
        elif self.logic == "AND":
            mask = self.df["collections"].apply(
                lambda x: all(
                    c in self._parse_collections(x)
                    for c in self.collection_names
                )
            )
        else:
            raise ValueError("Logic must be 'OR' or 'AND'.")

        filtered_df = self.df[mask]
        selected_columns = [p for p in self.properties if p in filtered_df.columns]
        self.filtered_df = filtered_df[selected_columns]

        try:
            self.filtered_df.to_csv(self.output_path, index=False)
        except Exception as e:
            raise IOError(f"Failed to write filtered data to CSV: {e}")

        return self

    def get_dataframe(self):
        return self.filtered_df.copy()

    def _parse_collections(self, value):
        if pd.isna(value):
            return set()
        return {c.strip() for c in re.split(r"[;|]", str(value)) if c.strip()}
