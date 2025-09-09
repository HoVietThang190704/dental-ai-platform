import os 
from pathlib import Path 

DATA_ROOT = Path(os.getenv("DATA_ROOT", "/app/data")).resolve();
RAW_DIR = DATA_ROOT / "raw";
PROCESSED_DIR = DATA_ROOT / "processed";
SPLITS_DIR = DATA_ROOT / "splits";
