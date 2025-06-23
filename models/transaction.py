from db.database import get_connection

class Transaction:
    def __init__(self, username, type, amount, category, note=None, date=None):
        self.username = username
        self.type = type  # "income" or "expense"
        self.amount = amount
        self.category = category
        self.note = note
        self.date = date  # should be in "YYYY-MM-DD" format or None

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO transactions (username, type, amount, category, note, date)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (self.username, self.type, self.amount, self.category, self.note, self.date)
        )
        conn.commit()
        conn.close()
