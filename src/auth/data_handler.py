import hashlib
import json
import os
from config.config import DATA_FILE_PATH, DATA_STORE_PATH


def load_users():
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_store_data(data):
    with open(DATA_STORE_PATH, "w") as file:
        json.dump(data, file, indent=2)


def load_store_data():
    if os.path.exists(DATA_STORE_PATH):
        try:
            with open(DATA_STORE_PATH, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_users(data):
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


def check_credentials(username, password, data):
    users = load_users()
    hashed_input_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    for user in users:
        if user['username'] == username:
            return hashed_input_password == user['password']
    return False


def check_username_exists(username, email, data):
    for user in data:
        if user['username'] == username or user['email'] == email:
            return True
    return False

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()