import unittest
import services.auth as auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpass"
        auth.register_user_test(self.username, self.password)

    def test_user_login_success(self):
        result = auth.login_user_test(self.username, self.password)
        self.assertTrue(result)

    def test_user_login_fail(self):
        result = auth.login_user_test(self.username, "wrongpass")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
