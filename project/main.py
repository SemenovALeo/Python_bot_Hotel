import telebot
import os
from telebot import types
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['hello-word'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")
