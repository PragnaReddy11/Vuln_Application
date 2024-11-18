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
    "' OR '1'='1' #",
    "admin' --",
    "admin' #",
]

def test_sql_injection():
    """
    Test the /login endpoint for SQL Injection vulnerabilities using POST requests.
    """
    # print("\n[SQL Injection Test on /login]")

    vulnerable = False
    for payload in sql_injection_payloads:
        # Send a POST request to /login with SQL injection payloads in the form data
        data = {'username': 'admin', 'password': payload}
        response = requests.post(f"{BASE_URL}/login", data=data)

        # Check for signs of SQL Injection vulnerability
        if response.status_code == 200 and ("Invalid credentials" not in response.text):
            # SQL injection might be present if login succeeds without valid credentials
            vulnerable = True
            # print(f"[!] SQL Injection detected with payload: {payload}")
        elif response.status_code == 401 and "Invalid credentials" in response.text:
            # If the response code is 401, it indicates invalid credentials
            # print(f"[+] No SQL Injection detected with payload: {payload}")
            return False
        elif response.status_code >= 400:
            # If the response code is 400 or 500, it indicates an error unrelated to SQLi
            # print(f"[Warning] Received error code {response.status_code} for payload: {payload}")
            return False
    
    if vulnerable:
        return False
        
    else:
        # print("================================================")
        # print("[+] No SQL Injection vulnerabilities detected.")
        return True

# Pattern to identify parameterized queries (safe pattern for SQLite queries)
safe_query_pattern_1 = re.compile(r"execute\(.+?,\s*\(.+?\)\)")
safe_query_pattern_2 = re.compile(r"\(.+?,\s*\[.+?\]\)")


def check_sql_injection_patch():
    """
    Checks if the SQL injection vulnerability has been patched by looking for parameterized
    query patterns in the code and alerting on unsafe patterns.
    """
    with open(FILE_PATH, 'r') as f:
        code = f.read()

    # Check for secure parameterized queries
    if safe_query_pattern_1.search(code):
        # print("[+] Secure parameterized queries detected.")
        return True
    elif safe_query_pattern_2.search(code):
        # print("[+] Secure parameterized queries detected.")
        return True
    else:
        return False

if __name__ == "__main__":
    # Run the SQL Injection test
    sqli_test1 = test_sql_injection()
    sqli_test2 = check_sql_injection_patch()

    if sqli_test1 and sqli_test2:
        print("================================================")
        print("✅ Check 4 - SQL Injection vulnerabilities remediation passed: +10 points")
    else:
        print("================================================")
        print("❌ Check 4 - SQL Injection vulnerabilities remediation failed: 0 points")