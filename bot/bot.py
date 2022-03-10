import telebot
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN_KEY"), parse_mode=None)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # if create_user(message.chat.username, message.chat.id):
    #     bot.reply_to(message, "+")
    # print(message)
    pass
