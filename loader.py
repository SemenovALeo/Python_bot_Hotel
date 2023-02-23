from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
