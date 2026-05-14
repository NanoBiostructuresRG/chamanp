# SPDX-License-Identifier: LGPL-3.0-or-later

from chamanp._utils.result_manager import ResultManager

class ReportWriter:
    def __init__(self, config):
        self.config = config

    def generate_phase2_report(self, **kwargs):
        content = self._build_content(**kwargs)
        report_path = f"{self.config.REPORTS_PATH}/report_dbprep_{kwargs['collection_tag']}.txt"
        manager = ResultManager(report_path)
        manager.write_results(content)
        return report_path

    def _build_content(self, total_input_size, total_after_dedup, stereo_removed_count,
                       target_collections, logic, final_count, retained_properties,
                       curated_csv, filtered_csv, metadata_csv, fingerprints_npy,
                       collection_tag, invalid_smiles_csv=None,
                       invalid_smiles_count=None, input_csv=None,
                       valid_molecules_count=None, fingerprint_radius=None,
                       fingerprint_bits=None):
        lines = [
            "# Pipeline Report - ML-stage: Input Preparation",
            "",
            f"Title: {', '.join(target_collections)} - Dataset Preparation",
            f"Tag: {collection_tag}",
            "----------------------------------------------------",
            f"Original database size:       {total_input_size}",
            f"Stereo-duplicates removed:    {stereo_removed_count}",
            f"Remaining after deduplication: {total_after_dedup}",
            "",
            f"Target collections:           {target_collections}",
            f"Logic:                        {logic}",
            f"Final compounds retained:     {final_count}",
        ]

        if invalid_smiles_count is not None:
            lines.append(f"Invalid SMILES rows:          {invalid_smiles_count}")

        if valid_molecules_count is not None:
            lines.append(f"Valid molecules fingerprinted: {valid_molecules_count}")

        lines += [
            "",
            "Execution metadata:",
            f"- Collection tag:    {collection_tag}",
        ]

        if input_csv:
            lines.append(f"- Input CSV:         {input_csv}")

        if fingerprint_radius is not None:
            lines.append(f"- Fingerprint radius: {fingerprint_radius}")

        if fingerprint_bits is not None:
            lines.append(f"- Fingerprint bits:   {fingerprint_bits}")

        lines += [
            "",
            "Properties retained:"
        ]

        lines += [f"- {p}" for p in retained_properties]

        lines += [
            "",
            "Output files:",
            f"- Curated CSV:       {curated_csv}",
            f"- Filtered CSV:      {filtered_csv}",
            f"- Metadata CSV:      {metadata_csv}",
            f"- Fingerprints NPY:  {fingerprints_npy}"
        ]

        if invalid_smiles_csv:
            lines.append(f"- Invalid SMILES CSV: {invalid_smiles_csv}")

        return "\n".join(lines)
