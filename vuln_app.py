import os
from flask import Flask, request, redirect, send_from_directory, render_template, url_for
import sqlite3

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hardcoded secret (bad practice)
ADMIN_PASSWORD = "admin"

# Persistent SQLite connection (rather than in-memory)
def get_db_connection():
    conn = sqlite3.connect('users.db')  # This creates a persistent SQLite database file
    return conn

# Initialize the database and insert initial users
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin')")
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user1', 'password123')")
    conn.commit()
    conn.close()

init_db()  # Initialize the database when the app starts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Hardcoded secret vulnerability
    if password == ADMIN_PASSWORD:
        return render_template('welcome.html', username="Admin")

    # Vulnerable SQL query - User input directly passed into SQL query (SQL Injection)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # Executing the query (dangerous!)
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(query)
        user = c.fetchone()
        conn.close()
        if user:
            return render_template('welcome.html', username=username)
        else:
            return "Invalid credentials"
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

# File upload functionality
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return f'File {filename} uploaded successfully!'

# Vulnerable search functionality with command injection (updated)
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']

    # Construct the file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], query)

    # Check if the file exists
    if os.path.exists(file_path):
        # Safely open the file and read its content
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
            return f"Search Results:<br><pre>{file_content}</pre>"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    else:
        return "File not found"

# Serve uploaded files (Potential XSS vulnerability when rendering file content)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Set host to 0.0.0.0 to make the app externally accessible on your local network
    app.run(debug=True, host='0.0.0.0', port=5001)
