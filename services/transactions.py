from datetime import datetime
from models.transaction import Transaction
from services.auth import get_current_user
from db.database import get_connection

def add_transaction():
    print("\n=== Add Transaction ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    type = input("Type (income/expense): ").strip().lower()
    if type not in ['income', 'expense']:
        print("Invalid type. Must be 'income' or 'expense'.")
        return

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Amount must be a number.")
        return

    category = input("Category: ")
    note = input("Note (optional): ")

    # Optional custom date input
    date_input = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    try:
        if date_input:
            date = datetime.strptime(date_input, "%Y-%m-%d").date().isoformat()
        else:
            date = datetime.now().date().isoformat()
    except ValueError:
        print("❌ Invalid date format.")
        return

    txn = Transaction(username, type, amount, category, note, date)
    txn.save()
    print(f"✅ {type.capitalize()} of ₹{amount} added on {date}.")

def view_transactions():
    print("\n=== Transaction History ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT id, date, type, amount, category, note FROM transactions
           WHERE username = ?
           ORDER BY date DESC''',
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    for row in rows:
        txn_id, date, t_type, amount, category, note = row
        print(f"[{txn_id}] {date} | {t_type.upper()} | ₹{amount} | {category} | {note}")

def delete_transaction():
    print("\n=== Delete Transaction ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    try:
        txn_id = int(input("Enter transaction ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ? AND username = ?", (txn_id, username))
    conn.commit()
    conn.close()
    print(f"✅ Transaction #{txn_id} deleted (if it existed).")

def update_transaction():
    print("\n=== Update Transaction ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    try:
        txn_id = int(input("Enter transaction ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, type, amount, category, note, date FROM transactions WHERE id = ? AND username = ?",
        (txn_id, username)
    )
    row = cursor.fetchone()

    if not row:
        print("Transaction not found or unauthorized.")
        conn.close()
        return

    _, current_type, current_amount, current_category, current_note, current_date = row

    new_type = input(f"Type [{current_type}]: ").strip().lower() or current_type
    if new_type not in ['income', 'expense']:
        print("Invalid type.")
        conn.close()
        return

    try:
        new_amount = input(f"Amount [{current_amount}]: ").strip()
        new_amount = float(new_amount) if new_amount else current_amount
    except ValueError:
        print("Amount must be a number.")
        conn.close()
        return

    new_category = input(f"Category [{current_category}]: ").strip() or current_category
    new_note = input(f"Note [{current_note or ''}]: ").strip() or current_note

    new_date_input = input(f"Date [{current_date}]: ").strip()
    try:
        new_date = datetime.strptime(new_date_input, "%Y-%m-%d").date().isoformat() if new_date_input else current_date
    except ValueError:
        print("Invalid date format.")
        conn.close()
        return

    cursor.execute('''
        UPDATE transactions
        SET type = ?, amount = ?, category = ?, note = ?, date = ?
        WHERE id = ? AND username = ?
    ''', (new_type, new_amount, new_category, new_note, new_date, txn_id, username))

    conn.commit()
    conn.close()
    print(f"✅ Transaction #{txn_id} updated.")

def monthly_report():
    print("\n=== Monthly Financial Report ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, type, SUM(amount)
        FROM transactions
        WHERE username = ?
        GROUP BY month, type
        ORDER BY month DESC
    ''', (username,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    summary = {}
    for month, t_type, total in rows:
        if month not in summary:
            summary[month] = {"income": 0.0, "expense": 0.0}
        summary[month][t_type] = total

    for month, data in summary.items():
        savings = data["income"] - data["expense"]
        print(f"{month}: Income ₹{data['income']}, Expense ₹{data['expense']}, Savings ₹{savings}")

def yearly_report():
    print("\n=== Yearly Financial Report ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT strftime('%Y', date) as year, type, SUM(amount)
        FROM transactions
        WHERE username = ?
        GROUP BY year, type
        ORDER BY year DESC
    ''', (username,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    summary = {}
    for year, t_type, total in rows:
        if year not in summary:
            summary[year] = {"income": 0.0, "expense": 0.0}
        summary[year][t_type] = total

    for year, data in summary.items():
        savings = data["income"] - data["expense"]
        print(f"{year}: Income ₹{data['income']}, Expense ₹{data['expense']}, Savings ₹{savings}")

def total_summary():
    print("\n=== Total Financial Summary ===")
    username = get_current_user()

    if not username:
        print("⚠️  No user is currently logged in. Please log in first.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT type, SUM(amount)
        FROM transactions
        WHERE username = ?
        GROUP BY type
    ''', (username,))
    rows = cursor.fetchall()
    conn.close()

    total_income = 0
    total_expense = 0
    for t_type, total in rows:
        if t_type == 'income':
            total_income = total
        elif t_type == 'expense':
            total_expense = total

    savings = total_income - total_expense
    print(f"Total Income: ₹{total_income}")
    print(f"Total Expense: ₹{total_expense}")
    print(f"Total Savings: ₹{savings}")
