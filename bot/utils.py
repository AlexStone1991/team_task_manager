from django.conf import settings
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import requests
from django.conf import settings

def send_telegram_message_sync(chat_id, message):
    """СИНХРОННАЯ отправка сообщения через Telegram Bot API"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки Telegram: {e}")
        return False

def get_user_tasks(user):
    """Получить задачи пользователя"""
    from tasks.models import Task
    tasks = Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress'])
    return tasks