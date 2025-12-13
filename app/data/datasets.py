import sqlite3
import pandas as pd
from app.data.db import connect_database
from app.data.schema import create_datasets_metadata_table

def insert_dataset(dataset_name, category, source, last_updated,
                   record_count, file_size_mb, uploaded_by, created_at):
    """Insert a new dataset metadata record and return the new row id (or None on error)."""
    conn = connect_database()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                       INSERT INTO datasets_metadata
                       (dataset_name, category, source, last_updated, record_count, file_size_mb, uploaded_by,
                        created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (dataset_name, category, source, last_updated, record_count, file_size_mb, uploaded_by,
                             created_at))
        conn.commit()
        last_id = cursor.lastrowid
        print("Inserted dataset metadata successfully.")
        return last_id
    except sqlite3.Error as e:
        print(f"Database error. Failed to insert dataset metadata: {e}")
        return None
    finally:
        conn.close()


def get_all_datasets():
    """Get all dataset metadata rows as a pandas DataFrame ordered by id descending."""
    conn = connect_database()

    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY incident_id DESC", conn)
    conn.close()
    return df


def update_dataset_record_count(conn, dataset_id, new_record_count):
    """Update dataset record_count by id. Returns number of rows affected."""
    cursor = conn.cursor()
    sql = "UPDATE datasets_metadata SET record_count = ? WHERE id = ?"
    try:
        cursor.execute(sql, (new_record_count, dataset_id))
        conn.commit()
        print("Updated dataset record_count successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to update dataset record_count: {e}")
        return 0


def delete_dataset(conn, dataset_id):
    """Delete dataset metadata row by id. Returns number of rows deleted."""
    cursor = conn.cursor()
    sql = "DELETE FROM datasets_metadata WHERE id = ?"
    try:
        cursor.execute(sql, (dataset_id,))
        conn.commit()
        print("Deleted dataset successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to delete dataset: {e}")
        return 0


# Analytical queries adapted for datasets_metadata table (similar style to incidents.py)
def get_datasets_by_category_count(conn):
    """
    Count datasets by category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_largest_datasets(conn, limit=5):
    """
    Return datasets with highest record_count.
    Uses: SELECT, FROM, ORDER BY, LIMIT
    """
    query = """
    SELECT dataset_name, record_count, file_size_mb, uploaded_by
    FROM datasets_metadata
    WHERE record_count IS NOT NULL
    ORDER BY record_count DESC
    LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df


def get_datasets_uploaded_by(conn, uploader):
    """
    Find datasets uploaded by a specific user.
    Uses: SELECT, FROM, WHERE, ORDER BY
    """
    query = """
    SELECT *
    FROM datasets_metadata
    WHERE uploaded_by = ?
    ORDER BY created_at DESC
    """
    df = pd.read_sql_query(query, conn, params=(uploader,))
    return df


# Test: Run analytical queries (same pattern as incidents.py)
if __name__ == "__main__":
    conn = connect_database()

    print("\n Datasets by Category:")
    df_by_cat = get_datasets_by_category_count(conn)
    print(df_by_cat)

    print("\n Largest Datasets:")
    df_largest = get_largest_datasets(conn, limit=5)
    print(df_largest)

    print("\n Datasets uploaded by 'data_scientist':")
    df_by_user = get_datasets_uploaded_by(conn, 'data_scientist')
    print(df_by_user)

    conn.close()