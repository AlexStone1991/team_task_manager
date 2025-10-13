from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()
router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start с async"""
    telegram_username = message.from_user.username
    
    try:
        # Используем sync_to_async для работы с Django ORM
        user = await sync_to_async(User.objects.get)(telegram_username=telegram_username)
        
        # Сохраняем chat_id
        user.telegram_chat_id = message.chat.id
        await sync_to_async(user.save)()
        
        await message.answer(
            f"👋 Привет, {user.first_name or user.username}!\n\n"
            f"Ты успешно привязал Telegram к системе управления задачами.\n\n"
            f"📋 Доступные команды:\n"
            f"/tasks - посмотреть мои задачи\n"
            f"/help - помощь"
        )
    except User.DoesNotExist:
        await message.answer(
            "❌ Пользователь не найден в системе.\n\n"
            "Чтобы работать с ботом:\n"
            "1. Зайди в админку http://127.0.0.1:8000/admin/\n"  
            "2. Найди своего пользователя\n"
            "3. В поле 'telegram_username' укажи: " + (telegram_username or "твой_username") + "\n"
            "4. Сохрани и напиши /start снова"
        )