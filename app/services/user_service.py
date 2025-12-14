import bcrypt
from app.data.db import connect_database, DATA_DIR
from app.data.schema import create_users_table, create_all_tables

file_path = DATA_DIR

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    conn = connect_database()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Insert into database
    # Insert new user
    cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                   (username, password_hash, role))
    conn.commit()
    conn.close()
    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Authenticate user."""
    conn = connect_database()
    cursor = conn.cursor()


    #Select id, username, password_hash, role so tuple layout is predictable
    cursor.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()
    if not user:
        return False, "User not found."

    stored_hash = user[1]  # password_hash is at index (0=username, 1=password_hash, 2=role)

    # Defensive check: ensure we have a string-like stored value
    if not isinstance(stored_hash, (bytes, str)):
        # Unexpected type in DB
        print(f"Debug: stored_hash for {username!r} has unexpected type: {type(stored_hash)} ({stored_hash!r})")
        return False, "Stored password invalid (contact admin)."

     # Try bcrypt.checkpw but catch exceptions when stored_hash isn't a valid bcrypt string
    try:
        # bcrypt expects bytes
        ok = bcrypt.checkpw(password.encode('utf-8'), str(stored_hash).encode('utf-8'))
    except (ValueError, TypeError) as e:
        # ValueError: Invalid salt -> means stored_hash isn't a valid bcrypt hash
        print(f"Warning: bcrypt failed for user {username!r}: {e!s}")
        print(f"Stored value: {stored_hash!r}")
        return False, "Stored password hash is invalid (please reset password)."

    if ok:
        return True, "Login successful!"
    else:
        return False, "Incorrect password."


def migrate_users_from_file(user_file_path= DATA_DIR/"users.txt"):
    """Migrate users from text file to database."""
    # ... migration logic ...
    conn = connect_database()
    create_users_table(conn)
    if not user_file_path.exists():
        print(f"File not found.{user_file_path}")
        print("No users to migrate.")
        return 0

    cursor = conn.cursor()
    migrated_count = 0

    with open(user_file_path,'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            #Parse line: username, password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                #Check for duplicates
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    continue

                #Insert user
                try:
                    # To Add Data To Database
                    cursor.execute("""INSERT INTO users(username, password_hash, role)
                                      VALUES (?,?,?)""", (username, password_hash, 'user')
                                   )  # ALWAYS USE ? PLACEHOLDERS
                    if cursor.rowcount > 0:
                        migrated_count += 1
                        print("Users migrated successfully.")
                except Exception as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f"Migrated {migrated_count} users from {user_file_path.name}.")
    conn.close()
    return migrated_count

#verify users were migrated
conn = connect_database()
create_all_tables(conn)
cursor = conn.cursor()

#Query all users
cursor.execute("""SELECT  username,role, password_hash FROM users""")
users = cursor.fetchall()

#to remove duplicates users
cursor.execute("""
DELETE FROM users
WHERE password_hash NOT IN (
    SELECT MIN(password_hash) FROM users GROUP BY username
);
""")
conn.commit()

print("Users in database:")
print(f"{'Username':<15}{'Password_hash':<40}{'Role':<10}")
print("-"*35)
for user in users:
    print(f"{user[0]:<15}{user[1]:<40}{user[2]:<10}")

print(f"\nTOTAL USERS: {len(users)}")
conn.close()

