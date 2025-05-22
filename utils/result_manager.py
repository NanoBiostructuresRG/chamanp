
import os
import logging
from datetime import datetime
import textwrap

class ResultManager:
    def __init__(self, output_file):
        self.output_file = output_file

        output_dir = os.path.dirname(self.output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    def _get_header(self):
        return textwrap.dedent(f"""            =====================================================
                                   CHAMANP
                 Curation-hierarchical analysis for molecular 
                        annotation of natural products
            -----------------------------------------------------
            Developer: Flavio F. Contreras-Torres
            Version: v1.0 - May, 2025. Oviedo
            Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            -----------------------------------------------------
            GitHub: https://github.com/NanoBiostructuresRG
            =====================================================
        """)

    def write_results(self, content):
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(self._get_header())
                f.write("\n")
                f.write(content)
        except Exception as e:
            raise IOError(f"Error writing results to '{self.output_file}': {e}")
