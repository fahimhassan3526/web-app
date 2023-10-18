from flask import Flask, render_template, request
import sqlite3
import os
import uuid

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    if not os.path.exists('data'):
        os.mkdir('data')
    db_file = 'data/banking_app.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            account_id TEXT,
            balance REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit', methods=['POST'])
def deposit():
    account_id = request.form['account_id']
    amount = float(request.form['amount'])
    db_file = 'data/banking_app.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
    current_balance = cursor.fetchone()
    if current_balance is None:
        return "Account not found."

    current_balance = current_balance[0]
    new_balance = current_balance + amount

    cursor.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (new_balance, account_id))
    conn.commit()
    conn.close()

    return f"Deposited {amount} to {account_id}. New balance: {new_balance}"

@app.route('/withdraw', methods=['POST'])
def withdraw():
    account_id = request.form['account_id']
    amount = float(request.form['amount'])
    db_file = 'data/banking_app.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
    current_balance = cursor.fetchone()
    if current_balance is None:
        return "Account not found."

    current_balance = current_balance[0]

    if current_balance >= amount:
        new_balance = current_balance - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (new_balance, account_id))
        conn.commit()
        conn.close()
        return f"Withdrew {amount} from {account_id}. New balance: {new_balance}"
    else:
        conn.close()
        return "Insufficient balance."

@app.route('/check_balance', methods=['GET'])
def check_balance():
    account_id = request.args.get('account_id')
    db_file = 'data/banking_app.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
    result = cursor.fetchone()
    conn.close()

    if result is not None:
        return f"Balance for {account_id}: {result[0]}"
    else:
        return "Account not found."

@app.route('/register', methods=['POST'])
def register():
    new_account_id = str(uuid.uuid4())  # Generate a unique account ID
    initial_balance = float(request.form.get('initial_balance', 0))  # Get initial balance from the request

    db_file = 'data/banking_app.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO accounts (account_id, balance) VALUES (?, ?)", (new_account_id, initial_balance))
    conn.commit()
    conn.close()

    return f"Registered new account with ID: {new_account_id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
