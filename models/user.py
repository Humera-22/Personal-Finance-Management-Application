import bcrypt
from db.database import get_connection

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (self.username, hashed_password)
            )
            conn.commit()
            print("User registered successfully.")
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()
