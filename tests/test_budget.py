import unittest
from models.budget import Budget
from services import auth
from db.database import get_connection

class TestBudget(unittest.TestCase):
    def setUp(self):
        self.username = "budget_user"
        auth.register_user_test(self.username, "pass123")
        self.budget = Budget(self.username, 6, 2025, 1000)
        self.budget.save()

    def test_set_and_get_budget(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT amount FROM budgets WHERE username = ? AND month = ? AND year = ?",
            (self.username, 6, 2025)
        )
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1000)
