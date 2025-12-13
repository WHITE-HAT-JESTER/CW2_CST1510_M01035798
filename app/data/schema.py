import pandas as pd  # pandas is a library for working with tables (DataFrames)
from .db import DatabaseManager
from pathlib import Path  # pathlib helps you work with file and folder paths
import re  # re is the regular expressions module for pattern matching in text

#
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "DATA"

CSV_PATHS = {
    "users": DATA_DIR / "users.txt",
    "cyber_incidents": DATA_DIR / "cyber_incidents.csv",
    "datasets_metadata": DATA_DIR / "datasets_metapidata.csv",
    "it_tickets": DATA_DIR / "it_tickets.csv",
}

# Table creation
def create_users_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY UNIQUE,
        password_hash TEXT NOT NULL UNIQUE,
        role TEXT DEFAULT 'user'
    );
    """
    conn.execute(sql)
    conn.commit()
    print("Created table: users")

def create_cyber_incidents_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT CHECK(severity IN ('Low', 'Medium', 'High','Critical')),
        status TEXT DEFAULT 'open',
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql)
    conn.commit()
    print("Created table: cyber_incidents")

def create_datasets_metadata_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        uploaded_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql)
    conn.commit()
    print("Created table: datasets_metadata")


def create_it_tickets_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT DEFAULT 'open',
        category TEXT,
        subject TEXT,
        description TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql)
    conn.commit()
    print("Created table: it_tickets")


def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

# This function shows the first few lines of a file if we can't read it properly
def preview_raw_file(path: Path, max_lines: int = 8):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")  # read the file as text
        lines = text.splitlines()  # split the text into lines
        print("RAW FILE PREVIEW (first lines):")
        for i, line in enumerate(lines[:max_lines]):
            print(f"{i+1:2}: {line!r}")  # print each line with its number
        if len(lines) > max_lines:
            print(f"... ({len(lines) - max_lines} more lines) ...")
    except Exception as e:
        print(f"Could not read raw file {path} for preview: {e}")

# This function checks if a string looks like a hashed password
def looks_like_hash(s: str) -> bool:
    if not isinstance(s, str):
        return False
    return bool(re.match(r"^\$2[aby]\$|\$argon2", s))  # regex pattern for common password hashes

# This function tries to read a users file and return a DataFrame with username and password_hash
def read_users(path: Path) -> pd.DataFrame:
    # First try: read the file with headers
    try:
        df = pd.read_csv(path, sep=None, engine='python', dtype=str)  # try reading with automatic separator
        cols = [c.lower() for c in df.columns]  # make column names lowercase
        rename_map = {}

        # Rename columns if needed
        if "password" in cols and "password_hash" not in cols:
            rename_map[df.columns[cols.index("password")]] = "password_hash"
        if "username" in cols:
            rename_map[df.columns[cols.index("username")]] = "username"

        df = df.rename(columns=rename_map)
        if "username" in df.columns and "password_hash" in df.columns:
            return df[["username", "password_hash"]]
    except Exception as e:
        print(f"First read attempt {path} failed:{e}")
        pass

    # Second try: read as whitespace-separated with no headers
    try:
        df = pd.read_csv(path, header=None, sep=r'\s+', engine='python', dtype=str)
        if df.shape[1] >= 2:
            df.columns = ["username", "password_hash"]
            return df[["username", "password_hash"]]
    except Exception as e:
        print(f"Second read attempt {path} failed:{e}")
        pass

    # Third try: read as comma-separated with no headers
    try:
        df = pd.read_csv(path, header=None, sep=",", dtype=str)
        if df.shape[1] >= 2:
            df.columns = ["username", "password_hash"]
            return df[["username", "password_hash"]]
    except Exception as e:
        print(f"Third read attempt {path} failed:{e}")
        pass

    # Final try: read line by line and split manually
    try:
        rows = []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            parts = re.split(r"\s+", line, maxsplit=1)
            if len(parts) == 2:
                rows.append(parts)
            else:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 2:
                    rows.append([parts[0], parts[1]])
                else:
                    rows.append([parts[0], ""])
        if rows:
            df = pd.DataFrame(rows, columns=["username", "password_hash"])
            if df["password_hash"].astype(bool).any():
                return df
    except Exception as e:
        print(f"Manually reading and splitting {path} failed:{e}")
        pass

    # If all attempts fail, show a preview and raise an error
    print("Failed to parse users file. Showing raw preview:")
    preview_raw_file(path, max_lines=12)
    raise ValueError("Could not parse users file into username and password_hash")

# This function loads the users table into the database
def load_users_table(conn, path: Path, replace: bool = False) -> int:
    try:
        df = read_users(path)

        # Validate password hashes
        valid_rows = df["password_hash"].str.startswith("$2b$")
        skipped = len(df) - valid_rows.sum()
        df = df[valid_rows]

        if "role" not in df.columns:
            df["role"] = "user"

        df = df[["username", "password_hash", "role"]]

        mode = "replace" if replace else "append"
        df.to_sql("users",
                  conn,
                  if_exists=mode,
                  index=False)

        print(f"Loaded users: {len(df)} rows")
        if skipped > 0:
            print(f"Skipped {skipped} rows with invalid password hashes")
        return len(df)

    except Exception as e:
        print(f"Error loading users from {path.name}: {e}")
        return 0


# This function tries to read a CSV file, and falls back to whitespace-separated if needed
def simple_read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.read_csv(path, header=None, sep=r'\s+', engine='python', dtype=str)

# This function removes empty unnamed columns from a DataFrame
def clean_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if str(col).lower().startswith("unnamed") and df[col].isna().all():
            df.drop(columns=[col], inplace=True)
    return df

# This function loads the cyber_incidents table into the database
def load_cyber_incidents_table(conn, path: Path) -> int:
    try:
        df = simple_read_csv(path)
        df.rename(columns={"incident_id": "id", "timestamp": "date", "category": "incident_type"}, inplace=True)
        df = clean_unnamed_columns(df)
        df["reported_by"] = df.get("reported_by", "unknown")  # add default if missing
        df["created_at"] = pd.Timestamp.now()  # add current timestamp
        expected = ["id", "date", "incident_type", "severity", "status", "description", "reported_by", "created_at"]
        df = df[expected]
        df.to_sql("cyber_incidents", conn, if_exists="replace", index=False)
        print(f"Loaded cyber_incidents: {len(df)} rows")
        return len(df)
    except Exception as e:
        print(f"Error loading cyber_incidents from {path.name}: {e}")
        return 0

# This function loads the datasets_metadata table into the database
def load_datasets_metadata_table(conn, path: Path) -> int:
    try:
        df = simple_read_csv(path)
        df.rename(columns={"dataset_id": "dataset_id", "name": "dataset_name"}, inplace=True)
        df = clean_unnamed_columns(df)
        df["category"] = df.get("category", "general")
        df["source"] = df.get("source", "unknown")
        df["last_updated"] = df.get("upload_date", pd.NaT)
        if "rows" in df.columns and "columns" in df.columns:
            df["record_count"] = pd.to_numeric(df["rows"], errors="coerce") * pd.to_numeric(df["columns"], errors="coerce")
        else:
            df["record_count"] = None
        df["file_size_mb"] = df.get("file_size_mb", 0.0)
        df["created_at"] = pd.Timestamp.now()
        expected = ["dataset_id", "dataset_name", "category", "source", "last_updated", "record_count", "file_size_mb", "uploaded_by", "created_at"]
        df = df[expected]
        df.to_sql("datasets_metadata", conn, if_exists="replace", index=False)
        print(f"Loaded datasets_metadata: {len(df)} rows")
        return len(df)
    except Exception as e:
        print(f"Error loading datasets_metadata from {path.name}: {e}")
        return 0

# This function loads the it_tickets table into the database
def load_it_tickets_table(conn, path: Path) -> int:
    try:
        df = simple_read_csv(path)
        df = clean_unnamed_columns(df)
        df["status"] = df.get("status", "open")
        df["category"] = df.get("category", "general")
        df["subject"] = df.get("subject", "unspecified")

        # Convert created_at to datetime and calculate resolved_date
        created = pd.to_datetime(df.get("created_at", pd.NaT), format="%y-%m-%d %H:%M", errors="coerce")
        if "resolution_time_hours" in df.columns:
            hours = pd.to_numeric(df["resolution_time_hours"], errors="coerce").fillna(0)
            df["resolved_date"] = (created + pd.to_timedelta(hours, unit="h")).dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            df["resolved_date"] = df.get("resolved_date", None)

        expected = ["ticket_id", "priority", "status", "category", "subject", "description", "created_at", "resolved_date", "assigned_to"]
        df = df[expected]
        df.to_sql("it_tickets", conn, if_exists="replace", index=False)
        print(f"Loaded it_tickets: {len(df)} rows")
        return len(df)
    except Exception as e:
        print(f"Error loading it_tickets from {path.name}: {e}")
    return 0

#Load all CSV data
def load_all_csv_data(conn):
    print("\nLoading CSV files into database tables...")

    loaders = {
        "cyber_incidents": load_cyber_incidents_table,
        "datasets_metadata": load_datasets_metadata_table,
        "it_tickets": load_it_tickets_table,
    }

    total_rows = 0
    for table_name, loader in loaders.items():
        csv_path = CSV_PATHS[table_name]
        if csv_path.exists():
            rows_loaded = loader(conn, csv_path)
            print(f"{table_name}: {rows_loaded} rows loaded")
            total_rows += rows_loaded
        else:
            print(f"{table_name}: File not found at {csv_path}")

    return total_rows


# Complete setup
def setup_database_complete():
    """Complete database setup"""
    print("=" * 60)
    print("SETTING UP COMPLETE DATABASE")
    print("=" * 60)

    # 1. Connect
    conn = DatabaseManager

    # 2. Create tables
    print("\n[1/3] Creating tables...")
    create_all_tables(conn)

    # 3. Load CSV data
    print("\n[2/3] Loading CSV data...")
    total_rows = load_all_csv_data(conn)

    # 4. Verify
    print("\n[3/3] Verifying setup...")
    cursor = conn.cursor()

    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\nDatabase Summary:")
    print(f"{'Table':<20} {'Rows':<10}")
    print("-" * 30)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<20} {count:<10}")

    conn.close()

    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print(f"\nDatabase location: {DATA_DIR}/intelligence_platform.db")

    return total_rows

# # Script entry point
if __name__ == "__main__":
    conn = DatabaseManager
    create_all_tables(conn)
    load_all_csv_data(conn)
    conn.close()