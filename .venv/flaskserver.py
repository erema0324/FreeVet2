from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from sql import init_db, save_question


app = Flask(__name__)
CORS(app)


@app.route('/webapp.html')
def render_templ():
    return render_template('webapp.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():

    action = request.form.get('action')
    print(action)
    subject = request.form.get('subject')
    print(subject)
    question = request.form.get('question')
    print(question)
    username = request.form.get('username')
    print(username)
    first_name = request.form.get('first_name')
    print(first_name)
    last_name = request.form.get('last_name')
    print(last_name)
    user_id = request.form.get('user_id')
    print(user_id)
    file_name = request.form.get('file_name')
    print(file_name)
    file = request.files['file']
    print(file)

    file_data = file.read()  # Получаем содержимое файла

    try:
        # Сохранение данных
        save_question(user_id, subject, question, file_name, file_data)

        # Отправка сообщения пользователю
        bot.send_message(user_id, "Ваш вопрос успешно отправлен ветеринарному врачу.")

        return jsonify({"message": "File and question saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Error saving data: {e}"}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
