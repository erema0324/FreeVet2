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


def create_bot(api_token):
    return telebot.TeleBot(api_token)


def webAppKeyboard(user_id, username, first_name, last_name):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    webAppTest = types.WebAppInfo(
        f"https://4e21-212-116-96-98.ngrok-free.app/webapp.html?user_id={user_id}&username={username}&first_name={first_name}&last_name={last_name}")
    one_butt = types.KeyboardButton(text="Open Web App", web_app=webAppTest)
    keyboard.add(one_butt)
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.username,
        "last_name": user.last_name if user.last_name else ""
    }

    save_user(user_data)
    logger.info(f"User {user.username} ({user.id}) started the bot with data: {user_data}")

    user_from_db = get_user(user.id)
    if user_from_db:
        bot.send_message(message.chat.id, 'Hello! Click the button to open the web app.',
                         reply_markup=webAppKeyboard(user.id, user.username, user.username, user.last_name))
    else:
        bot.send_message(message.chat.id, 'Hello! User data not found.')


if __name__ == "__main__":
    bot.infinity_polling()
