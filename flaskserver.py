from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT,
                request TEXT,
                status TEXT,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
    print("Database initialized successfully.")

@app.route('/upload', methods=['POST'])
def upload_question():
    data = request.get_json()
    subject = data.get('subject', '')
    message = data.get('message', '')
    user_id = 1  # Установите правильный user_id

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO requests (user_id, subject, request, status, date)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (user_id, subject, message, 'pending'))

    return jsonify({"status": "success"})

if __name__ == '__main__':
    init_db()
    app.run(port=5000)
