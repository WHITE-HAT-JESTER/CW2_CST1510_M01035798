import sqlite3
import pandas as pd
from my_app.data.db import connect_database

def insert_ticket(ticket_id, priority, subject, description, assigned_to,
                  category, status, resolved_date, created_at=None):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO it_tickets
            (ticket_id, priority, status, category, subject, description, resolved_date, assigned_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, priority, status, category, subject, description, resolved_date, assigned_to, created_at))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error. Failed to insert ticket: {e}")
        return None
    finally:
        conn.close()

def get_all_tickets():
    conn = connect_database()
    try:
        df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY ticket_id DESC", conn)
        return df
    except Exception as e:
        print(f"Database error. Failed to get tickets: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def update_ticket_status(ticket_id, new_status):
    """Update ticket status by id. Returns number of rows affected."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to update ticket status: {e}")
        return 0
    finally:
        conn.close()


def delete_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to delete ticket: {e}")
        return 0
    finally:
        conn.close()