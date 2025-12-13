import sqlite3
import pandas as pd
from my_app.app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()

    #Check if user exists
    sql=""" 
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by) 
        VALUES (?, ?, ?, ?, ?, ?)
            """

    try:
            cursor.execute(sql,(date, incident_type, severity, status, description, reported_by))
            conn.commit()
            print("Inserted incident successfully.")
            return cursor.lastrowid
    except sqlite3.Error as e:
            print(f"Database error. Failed to insert incident: {e}")
            return None
    finally:
        conn.close()
        pass

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC",
                           conn)
    conn.close()
    return df

def update_incident_status(conn, incident_id, new_status):
    """Update incident status."""
    cursor = conn.cursor()
    sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"

    try:
        cursor.execute(sql, (new_status, incident_id))
        conn.commit()
        print("Updated incident status successfully.")
        return cursor.rowcount #returns the number of rows affected
    except sqlite3.Error as e:
        print(f"Database error. Failed to update incident status: {e}")
        return 0

def delete_incident(conn, incident_id):
    """Delete incident from database."""
    cursor = conn.cursor()
    sql = "DELETE FROM cyber_incidents WHERE id = ?"

    try:
        cursor.execute(sql, (incident_id,))
        conn.commit()
        print("Deleted incident successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to delete incident: {e}")
        return 0

#Analytical Queries (The Big 6) - OPTIONAL it could be done with pandas

#1. **SELECT** — Choose what columns to return
#2. **FROM** — Specify the table
#3. **WHERE** — Filter individual rows
#4. **GROUP BY** — Group rows for aggregation
#5. **HAVING** — Filter aggregated groups
#6. **ORDER BY** — Sort the results

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

#print("\n Incidents by Type:")
#df_by_type = get_incidents_by_type_count(conn)
#print(df_by_type)

print("\n High Severity Incidents by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Incident Types with Many Cases (>5):")
df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()