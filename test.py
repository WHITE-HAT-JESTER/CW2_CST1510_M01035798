# Create a test file: test_db.py
import os

db_path = r"C:\Users\Personal\Desktop\CW2_M01035798_CST1510\DATA\intelligence_platform.db"
print(f"Database exists: {os.path.exists(db_path)}")
print(f"Size: {os.path.getsize(db_path) if os.path.exists(db_path) else 0} bytes")

# test_read_db.py
import sqlite3

db_path = r"C:\Users\Personal\Desktop\CW2_M01035798_CST1510\DATA\intelligence_platform.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

conn.close()