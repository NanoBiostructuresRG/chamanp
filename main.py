# main.py

import config
from core.base_pipeline import Pipeline

def main():
    pipeline = Pipeline(config=config)
    pipeline.run()

if __name__ == "__main__":
    main()
