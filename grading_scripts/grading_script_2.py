import re

file_path = "app.py"
points = 0

hardcoded_password_pattern = re.compile(r'ADMIN_PASSWORD\s*=\s*["\'].*["\']')
role_assignment_pattern = re.compile(r'role\s*=\s*["\']admin["\']\s*if\s*user\["is_admin"\]\s*else\s*["\']student["\']')
base_image_version_pattern = re.compile(r'FROM\s+[\w/]+:\s*1\.0\.1')

def detect_hardcoded_password(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if hardcoded_password_pattern.search(line):
                print("Hardcoded password still detected.")
                return True
    print("No hardcoded password found.")
    return False

def check_role_assignment(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if role_assignment_pattern.search(content):
            print("Role assignment logic is correct.")
            return True
    print("Role assignment logic is incorrect.")
    return False

def check_base_image_version(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if base_image_version_pattern.search(content):
            print("Base image version is correct.")
            return True
    print("Base image version is incorrect.")
    return False

def grade_script():
    global points

    if not detect_hardcoded_password(file_path):
        print("Step 1 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 1.")

    if check_role_assignment(file_path):
        print("Step 2 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 2.")

    if check_base_image_version(file_path):
        print("Step 3 complete. 10 points awarded.")
        points += 10
    else:
        print("Please redo Step 3.")

    print(f"Total Points: {points}")

grade_script()
