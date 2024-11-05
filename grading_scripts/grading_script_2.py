import re

# File paths
app_file_path = "../app.py"
docker_file_path = "../Dockerfile"  # Updated path for the Dockerfile
points = 0

# Regular expressions
hardcoded_password_pattern = re.compile(r'ADMIN_PASSWORD\s*=\s*["\'].*["\']')
role_assignment_pattern = re.compile(r'role\s*=\s*["\']admin["\']\s*if\s*user\["is_admin"\]\s*else\s*["\']student["\']')
base_image_version_pattern = re.compile(r'FROM\s+[\w/-]+:\s*1\.0\.1', re.IGNORECASE)


# Scan the file for hardcoded passwords
def detect_hardcoded_password(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if hardcoded_password_pattern.search(line):
                print("Hardcoded password still detected.")
                return True
    print("No hardcoded password found.")
    return False

# Check role assignment logic
def check_role_assignment(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if role_assignment_pattern.search(content):
            print("Role assignment logic is correct.")
            return True
    print("Role assignment logic is incorrect.")
    return False

# Check Docker base image version in Dockerfile
def check_base_image_version(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if base_image_version_pattern.search(content):
            print("Base image version is correct.")
            return True
    print("Base image version is incorrect.")
    return False

# Grading script
def grade_script():
    global points

    # Step 1: Check for hardcoded password in app.py
    if not detect_hardcoded_password(app_file_path):
        print("Step 1 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 1.")

    # Step 2: Check role assignment logic in app.py
    if check_role_assignment(app_file_path):
        print("Step 2 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 2.")

    # Step 3: Check Docker base image version in Dockerfile
    if check_base_image_version(docker_file_path):
        print("Step 3 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 3.")

    # Total points
    print(f"Total Points: {points}")

# Run the grading script
grade_script()
