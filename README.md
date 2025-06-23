# 💰 Personal Finance Management Application
This is a Python-based **Personal Finance Management Application** that helps users manage their budgets, track transactions, and securely store data in a SQLite database. It includes automated backups, user authentication, and a simple CLI-based interface.

## 📌 Features

### ✅ 1. User Registration and Authentication
- Unique usernames and secure password storage.
- User login functionality to access personalized data.

### 📥 2. Income and Expense Tracking
- Add, update, delete income and expense records.
- Categorize transactions (e.g., Food, Rent, Salary).

### 📊 3. Financial Reports
- Generate monthly/yearly financial reports.
- Calculate total income, expenses, and savings.

### 💡 4. Budgeting
- Set monthly budgets for categories.
- Get alerts when budget limits are exceeded.

### 🗃 5. Data Persistence
- Data stored securely in SQLite database.
- Automatic backup and restore functionality.

### 🧪 6. Testing and Documentation 
- Unit tests provided for key modules (`auth`, `budget`, `transactions`, etc.).
- Clear command-line interface.
- Simple setup with virtual environment.
- Easy-to-understand and maintainable codebase.

## 🚀 How to Run

1. **Clone the repo**

    ```bash
    git clone https://github.com/Humera-22/Personal-Finance-Management-Application.git
    cd Personal-Finance-Management-Application
    ```

2. **Create and activate virtual environment**

    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**

    ```bash
    python app.py
    ```

5. **🧪 Testing**

    ```bash
    python -m unittest discover -s tests
    ```

📽️ **Demo**  
You can download the output recording (`demo/demo.mp4`) to see how the app works.

👩‍💻 **Author**  
**Humera-22**  
GitHub: [@Humera-22](https://github.com/Humera-22)


