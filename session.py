import json, os
from datetime import datetime

SESSION_FILE = "session.json"

def create_session(username):
    data = {"user": username, "time": str(datetime.now()), "active": True}
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE) as f:
            data = json.load(f)
            return data if data.get("active") else None
    except:
        return None

def destroy_session():
    with open(SESSION_FILE, "w") as f:
        json.dump({"active": False}, f)
