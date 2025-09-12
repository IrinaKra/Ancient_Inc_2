import os
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "database.csv"))