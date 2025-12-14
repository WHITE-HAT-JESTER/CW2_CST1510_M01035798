import sqlite3
import pandas as pd
from my_app.data.db import connect_database

#Analytical Queries (The Big 6) - OPTIONAL it could be done with pandas

def insert_incident(date, incident_type, severity, status, description, reported_by):
    conn = connect_database()
    cursor = conn.cursor()
    sql="""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by) 
        VALUES (?, ?, ?, ?, ?, ?)
            """
    try:
        cursor.execute(sql,(date, incident_type, severity, status, description, reported_by))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error. Failed to insert incident: {e}")
        return None
    finally:
        conn.close()


def get_all_incidents():
    conn = connect_database()
    try:
        df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY incident_id DESC", conn)
        return df
    except Exception as e:
        print(f"Database error. Failed to get incidents: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE cyber_incidents SET status = ? WHERE incident_id = ?", (new_status, incident_id))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to update incident status: {e}")
        return 0
    finally:
        conn.close()


def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to delete incident: {e}")
        return 0
    finally:
        conn.close()