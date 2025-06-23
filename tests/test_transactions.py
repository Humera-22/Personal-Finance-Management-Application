import unittest
from models.transaction import Transaction
from services import auth
from db.database import get_connection

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.username = "test_tx_user"
        auth.register_user_test(self.username, "pass123")
        self.transaction = Transaction(
            username=self.username,
            type="income",
            amount=200,
            category="Salary",
            note="Test income",
            date="2025-06-17"
        )
        self.transaction.save()

    def test_add_transaction(self):
        # Check if transaction was saved
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE username = ?", (self.username,))
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

    def test_view_transaction(self):
        # Check if at least one transaction exists
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE username = ?", (self.username,))
        rows = cursor.fetchall()
        conn.close()
        self.assertGreater(len(rows), 0)
