import requests

# Define the base URL for the Flask application
BASE_URL = 'http://127.0.0.1:5000'

# SQL Injection payloads
sql_injection_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "admin' --",
    "admin' #",
    "'; DROP TABLE users; --"
]

def test_sql_injection():
    """
    Test the /login endpoint for SQL Injection vulnerabilities using POST requests.
    """
    print("\n[SQL Injection Test on /login]")

    vulnerable = False
    for payload in sql_injection_payloads:
        # Send a POST request to /login with SQL injection payloads in the form data
        data = {'username': 'admin', 'password': payload}
        response = requests.post(f"{BASE_URL}/login", data=data)

        # Check for signs of SQL Injection vulnerability
        if response.status_code == 200 and "Invalid credentials" not in response.text:
            # SQL injection might be present if login succeeds without valid credentials
            vulnerable = True
            print(f"[!] SQL Injection detected with payload: {payload}")
        elif response.status_code >= 400:
            # If the response code is 400 or 500, it indicates an error unrelated to SQLi
            print(f"[Warning] Received error code {response.status_code} for payload: {payload}")
    
    if not vulnerable:
        print("[-] No SQL Injection vulnerabilities detected.")

if __name__ == "__main__":
    # Run the SQL Injection test
    test_sql_injection()
