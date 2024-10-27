import sqlite3

# Persistent SQLite connection (rather than in-memory)
def get_db_connection():
    conn = sqlite3.connect('users.db')  # This creates a persistent SQLite database file
    return conn

# Initialize the database and insert initial users
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, is_admin INTEGER)''')
    c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('admin', 'admin', 1)")
    c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('student', 'tartans', 0)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    