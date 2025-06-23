# services/backup.py

import shutil
import os
from datetime import datetime

DB_NAME = "finance_app.db"
BACKUP_FOLDER = "backups"

def backup_database():
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"finance_backup_{timestamp}.db")
    try:
        shutil.copyfile(DB_NAME, backup_path)
        print(f"✅ Backup created at: {backup_path}")
    except Exception as e:
        print(f"❌ Failed to backup database: {e}")

def restore_database():
    if not os.path.exists(BACKUP_FOLDER):
        print("ℹ️ No backups found.")
        return

    backups = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith(".db")]
    if not backups:
        print("ℹ️ No backups found in the folder.")
        return

    print("\n📂 Available Backups:")
    for idx, fname in enumerate(backups, start=1):
        print(f"{idx}. {fname}")

    try:
        choice = int(input("Select a backup to restore (number): "))
        if 1 <= choice <= len(backups):
            selected = backups[choice - 1]
            backup_path = os.path.join(BACKUP_FOLDER, selected)
            shutil.copyfile(backup_path, DB_NAME)
            print("✅ Database restored successfully.")
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Invalid input.")
