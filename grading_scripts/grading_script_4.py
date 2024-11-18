import requests
import re
import os
# Path to the file to check (e.g., 'app.py' for the backend code)
FILE_PATH = os.path.join(os.path.dirname(__file__), '../app.py')

# Define the base URL for the Flask application
BASE_URL = 'http://localhost:5001'

# SQL Injection payloads
sql_injection_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "admin' --",
]


safe_query_pattern_1 = re.compile(r"execute\(.+?,\s*\(.+?\)\)")
safe_query_pattern_2 = re.compile(r"\(.+?,\s*\[.+?\]\)")

def test_sql_injection():
    """
    Test the /login endpoint for SQL Injection vulnerabilities using POST requests.
    """

    vulnerable = False
    for payload in sql_injection_payloads:
        data = {'username': 'admin', 'password': payload}
        response = requests.post(f"{BASE_URL}/login", data=data)

        if response.status_code == 200 and ("Invalid credentials" not in response.text):
            vulnerable = True
            break
            # print(f"[!] SQL Injection detected with payload: {payload}")
        elif response.status_code == 401 and "Invalid credentials" in response.text:
            vulnerable = False
        elif response.status_code >= 400:
            vulnerable = True
    
    return not vulnerable


# Pattern to identify parameterized queries (safe pattern for SQLite queries)
def check_sql_injection_patch():
    """
    Checks if the SQL injection vulnerability has been patched by looking for parameterized
    query patterns in the code and alerting on unsafe patterns.
    """

    with open(FILE_PATH, 'r') as f:
        code = f.read()

    if safe_query_pattern_1.search(code):
        return True
    elif safe_query_pattern_2.search(code):
        return True
    else:
        return False

if __name__ == "__main__":
    # Run the SQL Injection test
    if test_sql_injection():
        print("✅ Check #1 - Exploit no longer works: +10 points.")
    else:
        print("❌ Check #1 - Exploit still works: 0 points.")

    if check_sql_injection_patch():
        print("✅ Check #2 - SQL Injection patched: +10 points.")
    else:
        print("❌ Check #2 - SQL Injection not patched: 0 points.")
