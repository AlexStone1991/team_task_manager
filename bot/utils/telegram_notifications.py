import asyncio
from aiogram import Bot
from django.conf import settings

def send_telegram_message_sync(chat_id, text):
    """Синхронная отправка сообщения в Telegram"""
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
        async def send_message():
            await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        
        asyncio.run(send_message())
    except Exception as e:
        print(f"Ошибка отправки Telegram уведомления: {e}")

async def send_telegram_message_async(chat_id, text):
    """Асинхронная отправка сообщения в Telegram"""
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка отправки Telegram уведомления: {e}")