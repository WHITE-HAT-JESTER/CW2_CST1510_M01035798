from app.data.db import connect_database

def get_user_by_username(username):
    """Retrieve user by username"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):
    """Insert user into the database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",(username, password_hash, role))
    conn.commit()
    conn.close()

def delete_user(username):
    """Delete user from the database"""
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("""
                DELETE
                FROM users
                WHERE password_hash NOT IN (SELECT MIN(password_hash)
                                    FROM users
                                    GROUP BY username);
                """)
    conn.commit()
    conn.close()
