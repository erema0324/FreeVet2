import sqlite3

def init_db():
    try:
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
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

def save_user(user_data):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_data['id'], user_data['username'], user_data['first_name'], user_data['last_name']))
        print("User saved successfully.")
    except sqlite3.Error as e:
        print(f"Error saving user: {e}")

def get_user(user_id):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username, first_name, last_name FROM users WHERE id=?', (user_id,))
            user = cursor.fetchone()
        if user:
            print(f"User found: {user}")
        else:
            print("User not found.")
        return user
    except sqlite3.Error as e:
        print(f"Error retrieving user: {e}")
        return None

def get_user_stats(user_id):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM donations WHERE user_id=?', (user_id,))
            donations = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM requests WHERE user_id=?', (user_id,))
            requests = cursor.fetchone()[0]
        return {"donations": donations, "requests": requests}
    except sqlite3.Error as e:
        print(f"Error retrieving user stats: {e}")
        return {"donations": 0, "requests": 0}

def save_question(user_id, subject, question):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO requests (user_id, subject, request, status, date)
                VALUES (?, ?, ?, ?, datetime('now'))
            ''', (user_id, subject, question, 'pending'))
        print("Question saved successfully.")
    except sqlite3.Error as e:
        print(f"Error saving question: {e}")

def get_user_questions(user_id):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT subject, request, status FROM requests WHERE user_id=?', (user_id,))
            questions = cursor.fetchall()
            results = [{"subject": q[0], "request": q[1], "status": q[2]} for q in questions]
        return results
    except sqlite3.Error as e:
        print(f"Error retrieving user questions: {e}")
        return []

if __name__ == "__main__":
    init_db()
