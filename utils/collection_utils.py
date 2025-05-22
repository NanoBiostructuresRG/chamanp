
import json
import logging

class CollectionValidator:
    def __init__(self, taxonomy_json_path):
        self.taxonomy_json_path = taxonomy_json_path
        self.valid_collections = self._load_taxonomy()

    def _load_taxonomy(self):
        try:
            with open(self.taxonomy_json_path, "r", encoding="utf-8") as f:
                taxonomy = json.load(f)
            return set(taxonomy.get("entries", []))
        except FileNotFoundError:
            raise FileNotFoundError(f"Taxonomy file not found: {self.taxonomy_json_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in taxonomy file: {e}")

    def validate(self, target_collections):
        target_set = set(target_collections)
        unknown = target_set - self.valid_collections
        known = target_set & self.valid_collections

        if unknown:
            logging.warning(f"The following TARGET_COLLECTIONS are not recognized in taxonomy: {sorted(unknown)}")
        else:
            logging.info("All target collections are valid.")

        return sorted(known), sorted(unknown)
