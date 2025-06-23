# app.py

from db.database import initialize_db
from services.auth import register_user, login_user, clear_current_user, get_current_user
from services.transactions import (
    add_transaction,
    view_transactions,
    update_transaction,
    delete_transaction,
    monthly_report,
    yearly_report,
    total_summary
)
from services.budget import set_monthly_budget, view_current_budget
from services.backup import backup_database, restore_database  

def main_menu():
    initialize_db()
    while True:
        print("\n=== Personal Finance Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            register_user()
        elif choice == '2':
            if login_user():
                user_dashboard()
        elif choice == '3':
            clear_current_user()
            print("👋 Thank you for using Personal Finance Manager. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def user_dashboard():
    username = get_current_user()
    if not username:
        print("⚠️  No user is currently logged in.")
        return

    while True:
        print(f"\n=== User Dashboard ({username}) ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Monthly Report")
        print("6. Yearly Report")
        print("7. Total Summary")
        print("8. Set Monthly Budget")
        print("9. View Current Budget")
        print("10. Backup Data")            
        print("11. Restore Data")          
        print("12. Logout")                 

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            monthly_report()
        elif choice == '6':
            yearly_report()
        elif choice == '7':
            total_summary()
        elif choice == '8':
            set_monthly_budget()
        elif choice == '9':
            view_current_budget()
        elif choice == '10':
            backup_database()
        elif choice == '11':
            restore_database()
        elif choice == '12':
            clear_current_user()
            print("✅ Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()

