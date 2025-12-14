from db import connect_database
import sqlite3
import  pandas as pd

def get_user_by_username(username):
    """Retrieve user by username"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users where username = ?", (username,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Database Error. Failed to get user: {e}")
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

def get_users_by_role(role):
    """get by specific role."""
    conn = connect_database()
    try:
        query = "SELECT * FROM users WHERE role = ? ORDER BY username"
        df = pd.read_sql_query(query, conn, params=(role,))
        return df
    except Exception as e:
        print(f"Database error. Failed to get users by role: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_users_count_by_role():
    """Count users by role."""
    conn = connect_database()
    query = """
    SELECT role, COUNT(*) as count
    FROM users
    GROUP BY role
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def insert_user(username, password_hash, role='user'):
    """Insert user into the database"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",(username, password_hash, role))
        conn.commit()
        print("Inserted users into database")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database Error. Failed to insert user: {e}")
        return 0
    finally:
        conn.close()

def update_user_role(username, new_role):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
        print("Updated user role successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to update user role: {e}")
        return 0
    finally:
        conn.close()

def update_user_password(username, new_password_hash):
    """Update password hash."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?",
                      (new_password_hash, username))
        conn.commit()
        print("Updated user password successfully.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database error. Failed to update user password: {e}")
        return 0
    finally:
        conn.close()

def get_all_users():
    """Get all users as DataFrame."""
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
    """Delete user from the database"""
    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print(f"Deleted user '{username}' from database")
        return cur.rowcount
    except sqlite3.Error as e:
        print(f"Database Error. Failed to delete user: {e}")
        return 0
    finally:
        conn.close()

if __name__ == "__main__":
    print("\n Users by Role:")
    df_by_role = get_users_count_by_role()
    print(df_by_role)