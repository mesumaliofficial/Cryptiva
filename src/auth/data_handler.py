from config.config import DATA_FILE_PATH, DATA_STORE_PATH, ATTEMPTS_FILE
import hashlib
import json
import os
from datetime import datetime

def load_attempts():
    try:
        with open(ATTEMPTS_FILE, "r") as f:
            content = f.read()
            if not content.strip():
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []

    
def save_attempts(data):
    with open(ATTEMPTS_FILE, "w") as f:
        return json.dump(data, f, indent=4)

def get_user_attempt(username):
    attempts = load_attempts()
    for entry in attempts:
        if entry['username'] == username:
            return entry
    return {'username': username, 'failed_attempts': 0, "lock_time": None}

def update_user_attempt(username, failed_attempts, lock_time):
    attempts = load_attempts()
    found = False
    for entry in attempts:
        if entry['username'] == username:
            entry["failed_attempts"] = failed_attempts
            entry["lock_time"] = lock_time
            found = True
            break
    if not found:
        attempts.append({
            "username": username,
            'failed_attempts': failed_attempts,
            'lock_time': lock_time
        })
    save_attempts(attempts)


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
            stored_hash = user['password']
            stored_salt = bytes.fromhex(user['Salt'])

            password_bytes = password.encode()
            new_hash_bytes = hashlib.pbkdf2_hmac('sha256', password_bytes, stored_salt, 10000)
            new_hash = new_hash_bytes.hex()
            if new_hash == stored_hash:
                return True
            else:
                return False
    return False


def check_username_exists(username, email, data):
    for user in data:
        if user['username'] == username or user['email'] == email:
            return True
    return False

def hash_password(password, salt=None):
    password = password.encode()
    
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password, salt, 10000)
    return hash_bytes.hex(), salt.hex()
