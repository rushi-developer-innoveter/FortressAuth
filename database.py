import json
from datetime import datetime

USER_FILE = "users.json"
LOG_FILE = "logs.txt"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def log_event(username, success):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {username} | {'SUCCESS' if success else 'FAIL'}\n")
