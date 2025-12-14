from my_app.data.db import connect_database
import sqlite3
import pandas as pd

def get_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users where username = ?", (username,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Database Error. Failed to get user: {e}")
        return None
    finally:
        conn.close()


def get_all_users():
    conn = connect_database()
    try:
        df = pd.read_sql_query("SELECT * FROM users ORDER BY username", conn)
        return df
    except Exception as e:
        print(f"Database error. Failed to get users: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def delete_user(username):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database Error. Failed to delete user: {e}")
        return 0
    finally:
        conn.close()


def check_username_exists(username):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        count = cursor.fetchone()[0]
        return count > 0
    except sqlite3.Error as e:
        print(f"Database error. Failed to check username: {e}")
        return False
    finally:
        conn.close()


def insert_user(username, password_hash, role='user'):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database Error. Failed to insert user: {e}")
        return None
    finally:
        conn.close()