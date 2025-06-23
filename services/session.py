# services/session.py

import os

SESSION_FILE = "session.txt"

def login_session(username):
    with open(SESSION_FILE, "w") as f:
        f.write(username)

def logout_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def get_current_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        return f.read().strip()
