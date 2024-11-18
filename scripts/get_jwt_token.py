import datetime
import jwt
from jwt.algorithms import get_default_algorithms
import requests

BASE_URL = "http://127.0.0.1:5001"

def get_public_key():
    url = f'{BASE_URL}/public_key'
    response = requests.get(url)
    if response.status_code != 200:
        print("Please check server status.")
        return
    
    data = response.json()
    return data["public_key"]

if __name__ =="__main__":
    public_key = get_public_key()
    payload = {
        "role": "admin",
        "username": "admin",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(payload, public_key, algorithm="HS256")
    decoded_token = jwt.decode(token, public_key, algorithms=get_default_algorithms())

    if payload["role"] == decoded_token["role"]:
        print(token)
