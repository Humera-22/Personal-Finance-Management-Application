import unittest
import os
from services import backup

class TestBackup(unittest.TestCase):
    def test_create_and_restore_backup(self):
        # Create a backup
        backup.backup_database()

        # Check if a backup file was created
        backups = [f for f in os.listdir("backups") if f.endswith(".db")]
        self.assertGreater(len(backups), 0)

