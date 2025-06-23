from db.database import get_connection

class Budget:
    def __init__(self, username, month, year, amount):
        self.username = username
        self.month = month
        self.year = year
        self.amount = amount

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO budgets (username, month, year, amount)
            VALUES (?, ?, ?, ?)
        ''', (self.username, self.month, self.year, self.amount))
        conn.commit()
        conn.close()
