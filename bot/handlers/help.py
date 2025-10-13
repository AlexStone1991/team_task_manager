from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    """Справка по командам"""
    help_text = """
📋 <b>Доступные команды:</b>

/start - Начать работу с ботом
/tasks - Показать мои задачи  
/help - Эта справка

🔧 <b>Как работать:</b>
1. Администратор создает задачи в веб-интерфейсе
2. Бот присылает уведомления о новых задачах
3. Выполняй задачи и отмечай их в системе
"""
    await message.answer(help_text, parse_mode='HTML')