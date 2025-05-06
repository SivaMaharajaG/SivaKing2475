import sqlite3

def create_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_user_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_chat_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            message TEXT,
            sender TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

def get_user_role(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=?", (username,))
    role = c.fetchone()
    conn.close()
    return role[0] if role else None

def log_chat(username, role, message, sender):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (username, role, message, sender) VALUES (?, ?, ?, ?)", 
              (username, role, message, sender))
    conn.commit()
    conn.close()

def get_all_users():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT username, role FROM users")
    return c.fetchall()

def get_chat_history(username=None):
    conn = create_connection()
    c = conn.cursor()
    if username:
        c.execute("SELECT username, sender, message, timestamp FROM chat_history WHERE username=? ORDER BY timestamp", (username,))
    else:
        c.execute("SELECT username, sender, message, timestamp FROM chat_history ORDER BY timestamp")
    return c.fetchall()
