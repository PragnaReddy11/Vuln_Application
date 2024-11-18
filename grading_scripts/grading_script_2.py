import re

# File paths
app_file_path = "../app.py"
docker_file_path = "../Dockerfile"  # Updated path for the Dockerfile
# points = 0

# Regular expressions
hardcoded_password_pattern = re.compile(r'ADMIN_PASSWORD\s*=\s*["\'].*["\']')
role_assignment_pattern = re.compile(r'role\s*=\s*["\']admin["\']\s*if\s*user\["is_admin"\]\s*else\s*["\']student["\']')
base_image_version_pattern = re.compile(r'^FROM docker-registry\.local:5000/gr8scope-base:1\.0\.1', re.IGNORECASE) 


# Scan the file for hardcoded passwords
def detect_hardcoded_password(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if hardcoded_password_pattern.search(line):
                return True
    return False

# Check role assignment logic
def check_role_assignment(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if role_assignment_pattern.search(content):
            return True
    return False

# Check Docker base image version in Dockerfile
def check_base_image_version(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if base_image_version_pattern.search(content):
            print("Base image version is correct.")
            return True
    return False

# Grading script
def grade_script():
    global points

    # Step 1: Check for hardcoded password in app.py
    if not detect_hardcoded_password(app_file_path):
        print("✅ Check #1 - Hardcoded password successfully removed: +10 points.")
        # points += 10
    else:
        print("❌ Check #1 - Hardcoded password still exists: 0 points.")

    # Step 2: Check role assignment logic in app.py
    if check_role_assignment(app_file_path):
        print(" ✅ Check #2 - Admin verification logic is correct: +10 points.")
        # points += 10
    else:
        print("❌ Check #2 - Admin verification logic is incorrect: 0 points.")

    # Step 3: Check Docker base image version in Dockerfile
    if check_base_image_version(docker_file_path):
        print("✅ Check #3 - Docker base image version is correct: +10 points.")
        # points += 10
    else:
        print("❌ Check #3 - Docker base image version is incorrect: 0 points.")

# Run the grading script
grade_script()
