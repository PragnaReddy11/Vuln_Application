import os
from flask import (
    Flask,
    request,
    redirect,
    send_from_directory,
    render_template,
    url_for,
    jsonify,
    session,
    make_response,
)
import sqlite3
import datetime
import jwt
from jwt.algorithms import get_default_algorithms
from functools import wraps

app = Flask(__name__)

with open("./keys/private_key.pem", "rb") as f:
    PRIVATE_KEY = f.read()

with open("./keys/public_key.pem", "rb") as f:
    PUBLIC_KEY = f.read()

# Directory to store uploaded files
UPLOAD_FOLDER = "./submissions"
app.config["SECRET_KEY"] = PRIVATE_KEY

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Hardcoded secret (bad practice)
ADMIN_PASSWORD = "admin"


def get_db_connection():
    conn = sqlite3.connect("users.db")  # This creates a persistent SQLite database file
    conn.row_factory = sqlite3.Row
    return conn


def create_token(username, role):
    payload = {
        "role": role,
        "username": username,
        "exp": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=15),
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="EdDSA")
    return token


def verify_token(token):
    return jwt.decode(token, PUBLIC_KEY, algorithms=get_default_algorithms())


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return redirect(url_for("logout"))

        try:
            decoded_token = verify_token(token)
            if decoded_token and decoded_token["role"] == "admin":
                return f(*args, **kwargs)
        except Exception as e:
            pass
        return redirect(url_for("logout"))

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("logged_in" in session)
        if "logged_in" not in session:
            return render_template("login.html")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    token = request.cookies.get("token")
    if token:
        try:
            decoded_token = jwt.decode(
                token, PUBLIC_KEY, algorithms=get_default_algorithms()
            )
            if decoded_token and decoded_token["role"] == "admin":
                return render_template(
                    "home.html", username=session["username"], is_admin=True
                )
        except jwt.exceptions.ExpiredSignatureError as e:
            return redirect(url_for("login"))
        except Exception as e:
            print(e)
            pass
    return render_template("home.html", username=session["username"], is_admin=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    # Vulnerable SQL query - User input directly passed into SQL query (SQL Injection)
    #' OR '1'='1
    query = (
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    )

    # Executing the query (dangerous!)
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(query)
        user = c.fetchone()
        conn.close()
        if user:
            session["logged_in"] = True
            session["username"] = username
            role = "student"
            if user["password"] == ADMIN_PASSWORD:
                role = "admin"

            token = create_token(username=username, role=role)
            response = make_response(redirect(url_for("index")))
            response.set_cookie("token", token)
            return response
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except sqlite3.Error as e:
        return jsonify({"error": f"{e}"}), 500


# File upload functionality
@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload_submission():
    """Allow users to view a submission"""
    if request.method == "GET":
        return render_template("upload.html")

    elif request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = session["username"] + "_" + file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return f"File {filename} uploaded successfully!", 200


@app.route("/submissions", methods=["GET"])
@admin_required
def list_submissions():
    """Allow admin users to list submissions"""
    files = os.listdir(UPLOAD_FOLDER)
    print(files)
    return render_template("submissions.html", files=files)


@app.route("/submissions/<filename>", methods=["GET"])
@admin_required
def view_submission(filename):
    """Allow admin users to view a submission"""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/logout")
def logout():
    session.clear()
    response = redirect(url_for("login"))
    response.delete_cookie("token")
    return response


@app.route("/public_key")
def public_key():
    return jsonify({"public_key": PUBLIC_KEY.decode("utf-8")}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
