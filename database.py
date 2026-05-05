import sqlite3
import bcrypt

# 🔹 Create connection
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn


# 🔹 Create table (run once)
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    # 🔐 USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB
    )
    """)

    # 📂 UPLOADS TABLE (ADD HERE ✅)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        filename TEXT
    )
    """)

    conn.commit()
    conn.close()



# 🔹 Register new user

def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    # 🔐 Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# 🔹 Login user
def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user[2]

        # 🔥 Case 1: old plain text password
        if isinstance(stored_password, str) and not stored_password.startswith("$2b$"):
            if password == stored_password:
                return user

        # 🔥 Case 2: bcrypt password
        try:
            if isinstance(stored_password, str):
                stored_password = stored_password.encode()

            if bcrypt.checkpw(password.encode(), stored_password):
                return user
        except:
            return None

    return None

def update_password(username, new_password):
    conn = create_connection()
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

    cursor.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hashed, username)
    )

    conn.commit()
    conn.close()
def save_upload(username, filename):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO uploads (username, filename) VALUES (?, ?)",
        (username, filename)
    )

    conn.commit()
    conn.close()

def get_user_uploads(username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT filename FROM uploads WHERE username=?",
        (username,)
    )

    data = cursor.fetchall()
    conn.close()

    return data