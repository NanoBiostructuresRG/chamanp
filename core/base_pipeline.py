
# core/base_pipeline.py

import os
import logging
from core.curator import Curator
from core.filter import CompoundFilter
from core.fingerprints import FingerprintGenerator
from utils.collection_utils import CollectionValidator
from core.reporter import ReportWriter
from utils.path_manager import PathManager

os.makedirs("artifacts", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("artifacts/pipeline.log"),
        logging.StreamHandler()
    ]
)

class Pipeline:
    def __init__(self, config):
        self.config = config
        self.curated_df = None
        self.filtered_df = None
        self.valid_collections = []
        self.total_input_size = 0
        self.total_after_dedup = 0
        self.stereo_removed_count = 0

        self.paths = PathManager(tag=self.config.COLLECTION_TAG)

    def run(self):
        logging.info("Pipeline execution started.")
        self._create_directories()
        self._curate_data()
        self._validate_collections()
        self._filter_data()
        self._generate_fingerprints()
        self._write_report()
        logging.info("Pipeline execution completed.")

    def _create_directories(self):
        os.makedirs("artifacts", exist_ok=True)

    def _curate_data(self):
        logging.info("Curating raw input data...")
        curator = Curator(
            input_csv=self.config.DATABASE_PATH,
            output_csv=self.paths.curated(),
            keep_columns=self.config.SELECTED_PROPERTIES,
            remove_stereo_duplicates=self.config.REMOVE_STEREO_DUPLICATES
        ).load_and_clean()
        self.curated_df = curator.get_dataframe()
        with open(self.config.DATABASE_PATH, encoding="utf-8") as f:
            self.total_input_size = sum(1 for _ in f) - 1
        self.total_after_dedup = len(self.curated_df)
        self.stereo_removed_count = self.total_input_size - self.total_after_dedup
        logging.info(f"Total input rows: {self.total_input_size}, after deduplication: {self.total_after_dedup}")

    def _validate_collections(self):
        logging.info("Validating target collections...")
        validator = CollectionValidator(taxonomy_json_path=self.config.COLLECTION_TAXONOMY_PATH)
        self.valid_collections, _ = validator.validate(self.config.TARGET_COLLECTIONS)

    def _filter_data(self):
        logging.info("Filtering compounds by collection and properties...")
        compound_filter = CompoundFilter(
            df=self.curated_df,
            collection_names=self.valid_collections,
            logic=self.config.COLLECTION_LOGIC,
            properties=self.config.SELECTED_PROPERTIES,
            output_path=self.paths.filtered()
        ).apply_filters()
        self.filtered_df = compound_filter.get_dataframe()
        logging.info(f"Total compounds after filtering: {len(self.filtered_df)}")

    def _generate_fingerprints(self):
        logging.info("Generating molecular fingerprints...")
        FingerprintGenerator(
            input_csv=self.paths.filtered(),
            output_fp_file=self.paths.fingerprints(),
            output_metadata_file=self.paths.metadata(),
            output_invalid_file=self.paths.invalid_smiles()
        ).generate()
        logging.info(f"Fingerprints and metadata saved.")

    def _write_report(self):
        logging.info("Generating final report...")
        writer = ReportWriter(config=self.config)
        report_path = writer.generate_phase2_report(
            total_input_size=self.total_input_size,
            total_after_dedup=self.total_after_dedup,
            stereo_removed_count=self.stereo_removed_count,
            target_collections=self.valid_collections,
            logic=self.config.COLLECTION_LOGIC,
            final_count=len(self.filtered_df),
            retained_properties=self.config.SELECTED_PROPERTIES,
            curated_csv=self.paths.curated(),
            filtered_csv=self.paths.filtered(),
            metadata_csv=self.paths.metadata(),
            fingerprints_npy=self.paths.fingerprints(),
            collection_tag=self.config.COLLECTION_TAG
        )
        logging.info(f"Report saved to: {report_path}")
