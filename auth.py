import hashlib, os, hmac
from database import load_users, save_users, log_event

LOCK_LIMIT = 3

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return salt.hex(), key.hex()

def verify(stored_salt, stored_hash, password):
    salt = bytes.fromhex(stored_salt)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return hmac.compare_digest(key.hex(), stored_hash)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "User exists"

    salt, key = hash_password(password)
    users[username] = {"salt": salt, "password": key, "failed": 0, "locked": False}
    save_users(users)
    return True, "Registered"

def login_user(username, password):
    users = load_users()
    if username not in users:
        log_event(username, False)
        return False, "User not found"

    u = users[username]
    if u["locked"]:
        return False, "Account locked"

    if verify(u["salt"], u["password"], password):
        u["failed"] = 0
        save_users(users)
        log_event(username, True)
        return True, "Login successful"
    else:
        u["failed"] += 1
        if u["failed"] >= LOCK_LIMIT:
            u["locked"] = True
        save_users(users)
        log_event(username, False)
        return False, "Wrong password"
