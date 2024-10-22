import os
from flask import Flask, request, redirect, send_from_directory, render_template, url_for, jsonify, session
import sqlite3
import python_jwt as jwt 
import datetime
from jwcrypto import jwk

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = jwk.JWK.generate(kty='RSA', size=2048)

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
    # If the user is logged in, show the upload and search options
    if 'logged_in' in session and session['logged_in']:
        return render_template('home.html')
    # If not logged in, show the login page
    return render_template('login.html')

@app.route('/login', methods=['GET', "POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    # Hardcoded secret vulnerability
    if password == ADMIN_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('index'))
        # return render_template('welcome.html', username="Admin")

    # Vulnerable SQL query - User input directly passed into SQL query (SQL Injection)
    #' OR '1'='1
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
            return "Invalid credentials", 401
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

# Generate JWT token
@app.route('/test', methods=['GET'])
def test():
    # Get the username and password from the GET parameters
    username = request.args.get('username')
    password = request.args.get('password')
    if True:
        # Creating a JWT token with user claims
        token = jwt.generate_jwt({
            'user': username,
            'role': 'admin',  # Claims include 'role' that defines user privileges
        }, app.config['SECRET_KEY'], 'HS256', datetime.timedelta(minutes=5))
        return jsonify({'token': token})

# Protected route, only accessible to users with 'admin' role
@app.route('/protected', methods=['GET'])
def protected():
    token = request.args.get('token')
    if not token:
        return jsonify({'message': 'Token is missing'}), 403
    try:
        # Decode the token and check if the 'role' is 'admin'
        header,claims = jwt.verify_jwt(token, app.config['SECRET_KEY'], ['RS256'])
        
        return jsonify({'header': header, 'claims': claims})

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 403

# File upload functionality
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            return render_template('upload.html')
        return redirect(url_for('index'))

    elif request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully!', 200

# example of command injection
@app.route('/run', methods=['GET'])
def run_command():
    command = request.args.get('command')
    os.system(command)  # Vulnerable to command injection
    return f"Executed: {command}"

# Vulnerable search functionality with command injection (updated)
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            return render_template('search.html')
    
        return redirect(url_for('index'))
    
    elif request.method == 'POST':
    
        query = request.form['query']

        # Construct the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], query)

        command = f"ls {os.path.join(app.config['UPLOAD_FOLDER'], query)}"
        result = os.popen(command).read()
        # Return the result of the OS command execution
        return f"Search Results for: <b>{query}</b><br><pre>{result}</pre>"

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


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Set host to 0.0.0.0 to make the app externally accessible on your local network
    app.run(debug=True, host='0.0.0.0', port=5001)
