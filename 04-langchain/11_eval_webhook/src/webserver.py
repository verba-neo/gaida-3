# src/webserver.py

'''
uv add fastapi python-telegram-bot
'''
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from telegram import Bot

load_dotenv()

app = FastAPI()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

print(bot.get_updates())
# bot.send_message()