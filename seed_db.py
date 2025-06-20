import sqlite3

# Connect to the database (creates users.db if not exists)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                qualification TEXT,
                role TEXT
            )''')

# Insert sample admin and user
users = [
    ('admin', 'admin123', 'M.E CSE', 'admin'),
    ('user1', 'user123', 'B.E IT', 'user')
]

for u in users:
    try:
        c.execute("INSERT INTO users (username, password, qualification, role) VALUES (?, ?, ?, ?)", u)
    except:
        pass  # Ignore if user already exists

conn.commit()
conn.close()
print("Seeded users.")
