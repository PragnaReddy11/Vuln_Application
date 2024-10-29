@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    c = conn.cursor()
    try:
        # Using parameterized query to prevent SQL injection
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['logged_in'] = True
            return render_template('welcome.html', username=username)
        else:
            return "Invalid credentials", 401
    except sqlite3.Error as e:
        return f"An error occurred: {e}"