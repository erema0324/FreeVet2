# vetbot.py
import logging
import telebot
from telebot import types
import json
import sqlite3
from sql import save_user, get_user, save_question, get_user_questions, init_db
import time

API_TOKEN = '7214821564:AAGbG3JJyObd3cF8UNbMNibGSIxz_QMiZTU'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(API_TOKEN)


def webAppKeyboard(user_data):
    username, first_name, last_name = user_data
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    webAppTest = types.WebAppInfo(
        f"https://0fe4-212-116-96-98.ngrok-free.app/webapp.html?username={username}&first_name={first_name}&last_name={last_name}")
    one_butt = types.KeyboardButton(text="Open Web App", web_app=webAppTest)
    keyboard.add(one_butt)
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name if user.last_name else ""
    }

    save_user(user_data)
    logger.info(f"User {user.username} ({user.id}) started the bot with data: {user_data}")

    user_from_db = get_user(user.id)
    if user_from_db:
        bot.send_message(message.chat.id, 'Hello! Click the button to open the web app.',
                         reply_markup=webAppKeyboard(user_from_db))
    else:
        bot.send_message(message.chat.id, 'Hello! User data not found.')


@bot.message_handler(content_types="web_app_data")
def answer(webAppMes):
    logger.info("Received web app data:")
    logger.info(f"Full message: {webAppMes}")
    logger.info(f"Data from web app: {webAppMes.web_app_data.data}")

    data = webAppMes.web_app_data.data
    print(data)

    if data:
        try:
            event_data = json.loads(data)
            event = event_data.get("action")
            user_id = webAppMes.from_user.id
            query_id = webAppMes.web_app_data.query_id if hasattr(webAppMes.web_app_data, 'query_id') else None

            if event == "ask_question":
                subject = event_data.get("subject")
                question = event_data.get("question")

                try:
                    save_question(user_id, subject, question)
                    if query_id:
                        bot.answer_web_app_query(query_id,
                        json.dumps({"action": "question_received", "status": "success"}))
                    bot.send_message(user_id, "Ваш вопрос успешно отправлен ветеринарному врачу.")

                except Exception as e:
                    if query_id:
                        bot.answer_web_app_query(query_id, json.dumps({"action": "question_error", "status": "error"}))
                    logger.error(f"Error saving question: {e}")
                    bot.send_message(user_id,
                    "Произошла ошибка при отправке вашего вопроса. Пожалуйста, попробуйте еще раз.")

            elif event == "get_my_questions":
                try:
                    user_questions = get_user_questions(user_id)
                    if query_id:
                        bot.answer_web_app_query(query_id,
                                                 json.dumps({"action": "profile_data", "data": user_questions}))
                except Exception as e:
                    logger.error(f"Error retrieving user questions: {e}")
                    if query_id:
                        bot.answer_web_app_query(query_id, json.dumps({"action": "question_error", "status": "error"}))

            elif event == "donate":
                amount = event_data.get("amount")
                if query_id:
                    bot.answer_web_app_query(query_id, json.dumps({"action": "donate", "status": "success"}))

            logger.info(f"Event: {event}")
        except Exception as e:
            logger.error(f"Error parsing web app data: {e}")


if __name__ == "__main__":
    bot.infinity_polling()
