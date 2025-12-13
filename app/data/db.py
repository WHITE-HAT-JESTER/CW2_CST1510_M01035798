import sqlite3
from pathlib import Path

# Create DATA folder if it doesn't exist
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "DATA"
DB_PATH = DATA_DIR / "intelligence_platform.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))

class DatabaseManager:
    """Alternative class-based approach for database operations"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def connect(self):
        """Connect to SQLite database."""
        return sqlite3.connect(str(self.db_path))

    def execute_query(self, query, params=()):
        """Execute query and return results. Prevents SQL injection."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        if query.strip().lower().startswith(("insert", "update", "delete", "create", "drop")):
            conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result

if __name__ == "__main__":
    conn = connect_database()
    print(f"Database created at: {DB_PATH}")
    conn.close()