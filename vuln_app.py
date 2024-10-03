import os
from flask import Flask, request, redirect, send_from_directory, render_template_string
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
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CMU AIA File Upload Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                }
                .container {
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    width: 100%;
                    max-width: 600px;
                }
                h1 {
                    color: #764ba2;
                    text-align: center;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    margin-bottom: 2rem;
                }
                label {
                    margin-bottom: 0.5rem;
                    font-weight: bold;
                }
                input[type="text"], input[type="password"], input[type="file"], input[type="submit"] {
                    padding: 0.75rem;
                    margin-bottom: 1rem;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                input[type="submit"] {
                    background-color: #764ba2;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #667eea;
                }
                .note {
                    text-align: center;
                    font-style: italic;
                    color: #666;
                }
                .error {
                    color: red;
                    text-align: center;
                    margin-bottom: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>CMU AIA Class File Upload Server</h1>

                <!-- Login Form -->
                <h2>Login (Vulnerable to SQL Injection and Hardcoded Secret)</h2>
                <form method="POST" action="/login">
                    <label for="username">Username:</label>
                    <input type="text" name="username" id="username" placeholder="Enter your username" required />

                    <label for="password">Password:</label>
                    <input type="password" name="password" id="password" placeholder="Enter your password" required />

                    <input type="submit" value="Login" />
                </form>

                <!-- File Upload Form -->
                <h2>Upload a File</h2>
                <form method="POST" enctype="multipart/form-data" action="/upload">
                    <label for="file">Choose file to upload:</label>
                    <input type="file" name="file" id="file" required />

                    <input type="submit" value="Upload">
                </form>

                <!-- File Search Form -->
                <h2>Search for a File</h2>
                <form method="POST" action="/search">
                    <label for="query">Search query:</label>
                    <input type="text" name="query" id="query" placeholder="Enter file name to search" required />

                    <input type="submit" value="Search">
                </form>

                <div class="note">
                    <p>Note: This is a vulnerable application for testing purposes only.</p>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Hardcoded secret vulnerability
    if password == ADMIN_PASSWORD:
        return f"Welcome, Admin! (You logged in using a hardcoded secret)"

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
            return f"Welcome, {username}!"
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
