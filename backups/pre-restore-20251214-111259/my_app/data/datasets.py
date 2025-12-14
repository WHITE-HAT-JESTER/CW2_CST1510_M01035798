import pandas as pd
from my_app.data.db import connect_database


def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb, uploaded_by, created_at=None):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb, uploaded_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (dataset_name, category, source, last_updated, record_count, file_size_mb, uploaded_by, created_at))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Database error. Failed to insert dataset: {e}")
        return None
    finally:
        conn.close()


def get_all_datasets():
    conn = connect_database()
    try:
        df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY dataset_id DESC", conn)
        return df
    except Exception as e:
        print(f"Database error. Failed to get datasets: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def update_dataset_record_count(dataset_id, new_count):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE datasets_metadata SET record_count = ? WHERE dataset_id = ?", (new_count, dataset_id))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Database error. Failed to update dataset: {e}")
        return 0
    finally:
        conn.close()


def delete_dataset(dataset_id):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (dataset_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Database error. Failed to delete dataset: {e}")
        return 0
    finally:
        conn.close()