import sqlite3
import pandas as pd
from my_app.app.data.db import connect_database

def insert_ticket(ticket_id, priority, subject, description, assigned_to,
                  category, status, resolved_date, created_at=None):
    """Insert new ticket into it_tickets and return the new row id (or None on error)."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        # Use a parameterised INSERT to avoid SQL injection and to match the schema.
        cursor.execute("""
            INSERT INTO it_tickets
            (ticket_id, priority, status, category, subject, description, resolved_date, assigned_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, priority, status, category, subject, description, resolved_date, assigned_to, created_at))

        conn.commit()
        last_id = cursor.lastrowid
        print("Inserted ticket successfully.")
        return last_id
    except sqlite3.Error as e:
        print(f"Database error. Failed to insert ticket: {e}")
        return None
    finally:
        conn.close()


def get_all_tickets():
    """Get all tickets as a pandas DataFrame ordered by id descending."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY ticket_id DESC", conn)
    conn.close()
    return df


def update_ticket_status(conn, ticket_id, new_status):
    """Update ticket status by id. Returns number of rows affected."""
    cursor = conn.cursor()
    sql = "UPDATE it_tickets SET status = ? WHERE ticket_id = ?"
    try:
        cursor.execute(sql, (new_status, ticket_id))
        conn.commit()
        print("Updated ticket status successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to update ticket status: {e}")
        return 0


def delete_ticket(conn, ticket_id):
    """Delete ticket by id. Returns number of rows deleted."""
    cursor = conn.cursor()
    sql = "DELETE FROM it_tickets WHERE ticket_id = ?"
    try:
        cursor.execute(sql, (ticket_id,))
        conn.commit()
        print("Deleted ticket successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to delete ticket: {e}")
        return 0


# Analytical queries adapted for tickets table (similar style to incidents.py)
def get_tickets_by_priority_count(conn):
    """
    Count tickets by priority.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_open_tickets_by_assignee(conn):
    """
    Count open / in-progress tickets by assigned_to.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    WHERE status != 'Resolved'
    GROUP BY assigned_to
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_tickets_with_many_updates(conn, min_count=5):
    """
    Example aggregator: ticket_id occurrences (if duplicates inserted) - placeholder similar to incidents' HAVING example.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT ticket_id, COUNT(*) as count
    FROM it_tickets
    GROUP BY ticket_id
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df


# Test: Run analytical queries (same pattern as incidents.py)
if __name__ == "__main__":
    conn = connect_database()

    print("\n Tickets by Priority:")
    df_by_priority = get_tickets_by_priority_count(conn)
    print(df_by_priority)

    print("\n Open Tickets by Assignee:")
    df_open_by_assignee = get_open_tickets_by_assignee(conn)
    print(df_open_by_assignee)

    print("\n Tickets with Many Duplicates (>5):")
    df_many = get_tickets_with_many_updates(conn, min_count=5)
    print(df_many)

    conn.close()