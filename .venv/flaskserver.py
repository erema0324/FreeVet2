from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from sql import save_file_to_db

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
                file_name TEXT,
                file_data BLOB,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
    print("Database initialized successfully.")



@app.route('/webapp.html')
def render_templ():
    return render_template('webapp.html')



@app.route('/upload_file', methods=['POST'])
def upload_file():

    upload_folder = 'uploads'
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 800

    file = request.files['file']

    if file is None or file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 800


    file_path = os.path.join( upload_folder, file.filename)

    try:
        file.save(file_path)
        save_file_to_db(256509788, file)
        return jsonify({"status": "success", "message": "File uploaded successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "An error occurred while uploading the file"}), 500


oih
if __name__ == '__main__':
    init_db()
    app.run(port=5000)
