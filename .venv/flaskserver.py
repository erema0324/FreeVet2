from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from sql import init_db, save_question
import logging
from vetbot import create_bot

# API_TOKEN = '7214821564:AAGbG3JJyObd3cF8UNbMNibGSIxz_QMiZTU'
# bot = create_bot(API_TOKEN)

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webapp.html')
def render_templ():
    return render_template('webapp.html')


@app.route('/upload_question', methods=['POST'])
def upload_file():
    form_data = {key: request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.get(key) for key
                 in request.form}
    [logger.info(f"Field: {key}, Value: {value}") for key, value in form_data.items()]

    user_id, subject, question = (form_data.get(key, None) for key in
                                  ['user_id', 'subject', 'question'])

    files = request.files.getlist('files[]')
    file_data = [(file.filename, file.read()) for file in files]

    logger.info(' | '.join(file_name for file_name, _ in file_data))

    try:

        save_question(user_id, subject, question, file_data)
        # bot.send_message(user_id, "Ваш вопрос успешно отправлен ветеринарному врачу.")
        return jsonify({"message": "File and question saved successfully!"}), 200

    except Exception as e:
        # bot.send_message(user_id, "Произошла ошибка при отправке вашего вопроса. Пожалуйста, попробуйте еще раз.")
        logger.info({"error": f"Error saving data: {e}"})
        return jsonify({"error": f"Error saving data: {e}"}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
