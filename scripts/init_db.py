import sqlite3
import sys

# Persistent SQLite connection (rather than in-memory)
def get_db_connection():
    conn = sqlite3.connect('users.db')  # This creates a persistent SQLite database file
    return conn

# Initialize the database and insert initial users
def init_db(version: str = "1"):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, is_admin INTEGER)''')
    if version == "1":
        c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('admin', 'admin', 1)")
    else:
        c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('admin', '4dmin@flawscope#', 1)")
    c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('student', 'tartans', 0)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db(sys.argv[1])
    