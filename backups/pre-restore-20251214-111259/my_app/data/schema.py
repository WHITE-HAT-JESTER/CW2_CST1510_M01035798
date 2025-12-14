from my_app.data.db import connect_database, DATA_DIR
import pandas as pd
from pathlib import Path

CSV_PATHS = {
    'users': DATA_DIR / 'users.txt',
    'cyber_incidents': DATA_DIR / 'cyber_incidents.csv',
    'datasets_metadata': DATA_DIR / 'datasets_metadata.csv',
    'it_tickets': DATA_DIR / 'it_tickets.csv',
}


def create_users_table(conn):
    cursor = conn.cursor()
    create_users_table_sql = ("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        ) 
    """)
    cursor.execute(create_users_table_sql)
    conn.commit()
    print("Users Table created successfully")


def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    create_cyber_incidents_sql = ("""
        CREATE TABLE IF NOT EXISTS cyber_incidents(
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT DEFAULT 'open',
            description TEXT,
            reported_by TEXT
        )
    """)
    cursor.execute(create_cyber_incidents_sql)
    conn.commit()
    print('Cyber incidents table created')


def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)


def load_all_csv_data(conn):
    """Load CSV files listed in CSV_PATHS into the database if they exist."""
    for name, path in CSV_PATHS.items():
        if not Path(path).exists():
            print(f"CSV not found: {path}")
            continue
        try:
            df = pd.read_csv(path)
            df.to_sql(name if name != 'datasets_metadata' else 'datasets', conn, if_exists='replace', index=False)
            print(f"Loaded {name} into database from {path}")
        except Exception as e:
            print(f"Failed to load {path}: {e}")
