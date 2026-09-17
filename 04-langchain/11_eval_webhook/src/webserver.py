# src/webserver.py

'''
uv add fastapi python-telegram-bot
'''
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks, Header
from telegram import Bot, Update

load_dotenv()

app = FastAPI()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

@app.post('/telegram/webhook')  # localhost:2024/telegram/webhook
async def telegram(
    request: Request,
    background_tasks: BackgroundTasks,
):

    payload = await request.json()
    update = Update.de_json(payload, bot)
    message = update.message

    print('-------------------------------')
    print(message.chat.id, message.text)
    print('-------------------------------')

    await bot.send_message(
        chat_id=message.chat.id,
        text=message.text
    )

    return {'ok': True}