import sqlite3
import pandas as pd  # pandas is a library for working with tables (DataFrames)
from my_app.data.db import connect_database
from pathlib import Path  # pathlib helps you work with file and folder paths
import re

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