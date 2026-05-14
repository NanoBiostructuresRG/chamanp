# SPDX-License-Identifier: LGPL-3.0-or-later
# main.py

import config
from core.base_pipeline import Pipeline
from chamanp._core.preflight import validate_config

def main():
    validate_config(config)
    pipeline = Pipeline(config=config)
    pipeline.run()

if __name__ == "__main__":
    main()
