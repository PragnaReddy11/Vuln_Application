import base64
import datetime
import json
import jwt
import re
import requests

BASE_URL = "http://127.0.0.1:5001"
BASE_APP_PATH = "/home/student/gr8scope"
APP_PATH = f"{BASE_APP_PATH}/app.py"
REQ_PATH = f"{BASE_APP_PATH}/requirements.txt"
DOCKER_PATH = f"{BASE_APP_PATH}/Dockerfile"


def get_public_key():
    url = f'{BASE_URL}/public_key'
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Check #1 - Please check server status: 0 points.")
        return
    
    data = response.json()
    return data["public_key"]


def get_jwt_token(public_key: str):
    payload = {
        "role": "admin",
        "username": "admin",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(payload, public_key, algorithm='HS256')
    return token


def get_session_token():
    session = requests.Session()
    url = f'{BASE_URL}/login'
    data = 'eyJ1c2VybmFtZSI6ICJzdHVkZW50IiwgInBhc3N3b3JkIjogInRhcnRhbnMifQ=='

    data = base64.b64decode(data.encode('utf-8'))
    login_data = json.loads(data)
    response = session.post(url, data=login_data)
    if response.status_code != 200:
        print("❌ Check #1 - Please check server status: 0 points.")
        return
    return session.cookies.get("session")


def exploit(jwt_token: str, session_token:str):
    url = f'{BASE_URL}/submissions'
    cookies = {'token': jwt_token, 'session': session_token}
    response = requests.get(url, cookies=cookies, allow_redirects=False)

    if response.status_code == 302:
        print("✅ Check #1 - Exploit no longer works: +10 points.")
        return 
    
    print("❌ Check #1 - Exploit still works: 0 points.")
    return


def check_code():
    vuln_regex = re.compile(r"jwt\.decode\(.*algorithms=get_default_algorithms\(\).*\)")
    patch_regex = re.compile(r"jwt\.decode\(.*algorithms=\[('|\")EdDSA('|\")\].*\)")
    with open(APP_PATH, 'r') as f:
        for line in f:
            if vuln_regex.search(line):
                print("❌ Check #2 - JWT vulnerability detected in code: 0 points.")
                return 
    
    with open(APP_PATH, 'r') as f:
        for line in f:
            if patch_regex.search(line):
                print("✅ Check #2 - Code successfully patched: +10 points.")
    return


def check_requirements():
    old_jwt_regex = re.compile(r"PyJWT==2\.3\..*")
    new_jwt_regex = re.compile(r"PyJWT==2\.4\.0")
    with open(REQ_PATH, 'r') as f:
        content = f.read()
        if old_jwt_regex.search(content):
            print("❌ Check #3 - Dependencies are outdated and vulnerable: 0 points.")
            return
        
    with open(REQ_PATH, 'r') as f:
        content = f.read()
        if new_jwt_regex.search(content):
            print("✅ Check #3 - Requirements successfully updated: +10 points.")
    return


def check_docker_image():
    old_base_regex = re.compile(r"FROM .*:1\.0\.1")
    new_base_regex = re.compile(r"FROM .*:1\.0\.2")
    with open(DOCKER_PATH, 'r') as f:
        content = f.read()
        if old_base_regex.search(content):
            print("❌ Check #4 - Base image is outdated and vulnerable: 0 points.")
            return
    
    with open(DOCKER_PATH, 'r') as f:
        content = f.read()
        if new_base_regex.search(content):
            print("✅ Check #4 - Base image successfully updated: +10 points.")
    return


def main():
    public_key = get_public_key()
    if public_key is None:
        return
    
    jwt_token = get_jwt_token(public_key)
    session_token = get_session_token()
    if jwt_token is None or session_token is None:
        return

    exploit(jwt_token, session_token)
    check_code()
    check_requirements()
    check_docker_image()

if __name__ == "__main__":
    main()
