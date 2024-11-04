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
        print("Please check server status.")
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


def get_session_token():
    session = requests.Session()
    url = f'{BASE_URL}/login'
    data = 'eyJ1c2VybmFtZSI6ICJzdHVkZW50IiwgInBhc3N3b3JkIjogInRhcnRhbnMifQ=='

    data = base64.b64decode(data.encode('utf-8'))
    login_data = json.loads(data)
    response = session.post(url, data=login_data)
    if response.status_code != 200:
        print("Please check server status.")
        return
    return session.cookies.get("session")


def exploit(jwt_token: str, session_token:str):
    url = f'{BASE_URL}/submissions'
    cookies = {'token': jwt_token, 'session': session_token}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        print("Exploit still works. Please check your patch.")
        return 
    
    print("Exploit no longer works (+10)")


def check_code():
    vuln_regex = re.compile(r"jwt\.decode\(.*algorithms=get_default_algorithms\(\).*\)")
    patch_regex = re.compile(r"jwt\.decode\(.*algorithms=\[('|\")EdDSA('|\")\].*\)")
    with open(APP_PATH, 'r') as f:
        for line in f:
            if vuln_regex.search(line):
                print("JWT vulnerability detected in code.")
                return
    
    with open(APP_PATH, 'r') as f:
        for line in f:
            if patch_regex.search(line):
                print("Code successfully patched.")
    return


def check_requirements():
    old_jwt_regex = re.compile(r"PyJWT==2\.3\..*")
    new_jwt_regex = re.compile(r"PyJWT==2\.4\.0")
    with open(REQ_PATH, 'r') as f:
        content = f.read()
        if old_jwt_regex.search(content):
            print('App dependencies are outdated and vulnerable.')
            return
        
    with open(REQ_PATH, 'r') as f:
        content = f.read()
        if new_jwt_regex.search(content):
            print('Requirements successfully updated.')
    return


def check_docker_image():
    old_base_regex = re.compile(r"FROM gr8scope:1\.0\.0")
    new_base_regex = re.compile(r"ROM gr8scope:1\.0\.2")
    with open(DOCKER_PATH, 'r') as f:
        content = f.read()
        if old_base_regex.search(content):
            print('Base image is outdated and vulnerable.')
            return
    
    with open(DOCKER_PATH, 'r') as f:
        content = f.read()
        if new_base_regex.search(content):
            print('Base image successfully updated.')
    return


if __name__ == "__main__":
    public_key = get_public_key()
    jwt_token = get_jwt_token(public_key)
    session_token = get_session_token()

    exploit(jwt_token, session_token)
    check_code()
    check_requirements()
    check_docker_image()
