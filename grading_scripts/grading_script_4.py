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
            break
            # print(f"[!] SQL Injection detected with payload: {payload}")
        elif response.status_code == 401 and "Invalid credentials" in response.text:
            # If the response code is 401, it indicates invalid credentials
            # print(f"[+] No SQL Injection detected with payload: {payload}")
            vulnerable = False
        elif response.status_code >= 400:
            # If the response code is 400 or 500, it indicates an error unrelated to SQLi
            # print(f"[Warning] Received error code {response.status_code} for payload: {payload}")
            vulnerable = True
            break
    
    if vulnerable:
        return False
        
    else:
        # print("================================================")
        # print("[+] No SQL Injection vulnerabilities detected.")
        return True


if __name__ == "__main__":
    # Run the SQL Injection test
    points = 0
    sqli_test = test_sql_injection()

    if sqli_test:
        points += 10
        print("✅ Check 1 - SQL Injection vulnerabilities remediation passed: +10 points")
    else:
        print("❌ Check 1 - SQL Injection vulnerabilities remediation failed: 0 points")

    print(f"Total points: {points}/10")