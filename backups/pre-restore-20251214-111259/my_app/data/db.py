import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "DATA"
DB_PATH = DATA_DIR / "intelligence_platform.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

print("my_app.data.db: initialized")
print(f"Project root: {PROJECT_ROOT}")
print(f"DATA folder: {DATA_DIR.resolve()}")
print(f"Database path: {DB_PATH.resolve()}")


def connect_database(db_path=DB_PATH, create_if_missing=True):
    db_path = Path(db_path)
    if not db_path.exists() and not create_if_missing:
        raise FileNotFoundError(f"Database file does not exist at: {db_path}")
    return sqlite3.connect(str(db_path))


if __name__ == "__main__":
    conn = connect_database()
    print(f"Opened database at: {DB_PATH.resolve()}")
    conn.close()