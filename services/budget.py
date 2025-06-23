from models.budget import Budget
from db.database import get_connection
from services.auth import get_current_user
from datetime import datetime

def set_monthly_budget():
    print("\n=== Set Monthly Budget ===")
    username = get_current_user()
    if not username:
        print("⚠️  Please log in first.")
        return

    try:
        year = int(input("Enter year (e.g., 2025): "))
        month = int(input("Enter month (1-12): "))
        amount = float(input("Enter budget amount: ₹"))
    except ValueError:
        print("❌ Invalid input.")
        return

    b = Budget(username, month, year, amount)
    b.save()
    print(f"✅ Budget of ₹{amount} set for {month}/{year}.")

def view_current_budget():
    print("\n=== Current Month Budget Overview ===")
    username = get_current_user()
    if not username:
        print("⚠️  Please log in first.")
        return

    today = datetime.today()
    month, year = today.month, today.year

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT amount FROM budgets
        WHERE username = ? AND month = ? AND year = ?
    ''', (username, month, year))
    row = cursor.fetchone()

    if not row:
        print("ℹ️  No budget set for this month.")
        return

    budget_amount = row[0]

    cursor.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE username = ? AND type = 'expense'
        AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (username, str(year), f"{month:02d}"))

    total_expense = cursor.fetchone()[0] or 0
    remaining = budget_amount - total_expense

    print(f"📅 Month: {month}/{year}")
    print(f"💰 Budget: ₹{budget_amount}")
    print(f"🧾 Spent: ₹{total_expense}")
    print(f"📉 Remaining: ₹{remaining}")
    if remaining < 0:
        print("⚠️ Budget exceeded!")
