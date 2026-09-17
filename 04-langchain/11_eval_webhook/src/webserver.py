# src/webserver.py

'''
uv add fastapi python-telegram-bot
'''
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks, Header
from telegram import Bot, Update

from src.app import agent

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

    result = await agent.ainvoke({
        'messages': [
            {'role': 'user', 'content': message.text}
        ]
    })

    agent_msg = result['messages'][-1].content
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=agent_msg
    )

    return {'ok': True}


@app.post('/slack/webhook')  # localhost:2024/telegram/webhook
async def slack(
    request: Request,
    background_tasks: BackgroundTasks,
):

    # SLACK 메세지 받기
    

    # agent 호출하기
    result = await agent.ainvoke({
        'messages': [
            {'role': 'user', 'content': "슬랙에서온메세지"}
        ]
    })
    #
    agent_msg = result['messages'][-1].content

    # SLACK 메세지 보내기

    return {'ok': True}