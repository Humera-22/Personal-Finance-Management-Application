import sqlite3
import os

def connect_db(db_name):
    if not os.path.exists(db_name):
        print(f"❌ Database file '{db_name}' not found.")
        return None
    return sqlite3.connect(db_name)

def show_users(cursor):
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("\n👤 Users:")
    for user in users:
        print(user)

def show_transactions(cursor):
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    print("\n💸 Transactions:")
    for tx in transactions:
        print(tx)

def show_budgets(cursor):
    cursor.execute("SELECT * FROM budgets")
    budgets = cursor.fetchall()
    print("\n📊 Budgets:")
    for b in budgets:
        print(b)

def show_transaction_count(cursor):
    cursor.execute("""
        SELECT u.username, COUNT(t.id) as total_transactions
        FROM users u
        LEFT JOIN transactions t ON u.username = t.username
        GROUP BY u.username
    """)
    results = cursor.fetchall()
    print("\n📈 Transaction Count per User:")
    for username, count in results:
        print(f"{username} — {count} transaction(s)")

def main():
    db_name = input("Enter database filename (e.g., finance_app.db or backup .db): ").strip()
    conn = connect_db(db_name)
    if not conn:
        return
    cursor = conn.cursor()

    show_users(cursor)
    show_transactions(cursor)
    show_budgets(cursor)
    show_transaction_count(cursor)

    conn.close()

if __name__ == "__main__":
    main()

