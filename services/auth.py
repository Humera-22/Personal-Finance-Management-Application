import re
import os
import sqlite3
import bcrypt
from models.user import User
from db.database import get_connection

SESSION_FILE = "current_user.txt"

def register_user():
    print("\n=== User Registration ===")
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()

    if len(password) < 6:
        print("❌ Password must be at least 6 characters long.")
        return

    if re.search(r'[^a-zA-Z0-9]', password):
        print("❌ Password must not contain special characters.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        print("❌ Username already exists.")
        return

    user = User(username, password)
    user.save()
    print("✅ Registration successful. You can now log in.")

def login_user():
    print("\n=== User Login ===")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                login_session(username)
                print(f"✅ Login successful. Welcome, {username}!")
                return True
            else:
                print("❌ Incorrect password.")
        else:
            print("❌ User not found.")
    except Exception as e:
        print("⚠️  Error during login:", e)
    finally:
        conn.close()

    return False

def login_session(username):
    """Save current user session."""
    try:
        with open(SESSION_FILE, "w") as f:
            f.write(username)
    except Exception as e:
        print(f"⚠️  Failed to save session: {e}")

def get_current_user():
    """Get current logged-in user."""
    try:
        with open(SESSION_FILE, "r") as f:
            user = f.read().strip()
            return user if user else None
    except FileNotFoundError:
        return None

def clear_current_user():
    """Log out the current user."""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception as e:
        print(f"⚠️  Failed to clear session: {e}")

def register_user_test(username, password):
    """Non-interactive version for testing purposes."""
    if len(password) < 6 or re.search(r'[^a-zA-Z0-9]', password):
        return False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False

    user = User(username, password)
    user.save()
    conn.close()
    return True

def login_user_test(username, password):
    """Non-interactive login function for testing."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8')

            return bcrypt.checkpw(password.encode('utf-8'), stored_password)
        return False
    except Exception:
        return False
    finally:
        conn.close()
