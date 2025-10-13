from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()
router = Router()

@router.message(Command("tasks"))
async def show_tasks(message: types.Message):
    """Показать задачи пользователя с async"""
    telegram_username = message.from_user.username
    
    try:
        user = await sync_to_async(User.objects.get)(telegram_username=telegram_username)
        
        # Получаем задачи пользователя
        from tasks.models import Task
        tasks = await sync_to_async(list)(Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress']))
        
        if not tasks:
            await message.answer("✅ У тебя нет активных задач!")
            return
        
        response = "📋 <b>Твои задачи:</b>\n\n"
        for task in tasks:
            status_icon = "⏳" if task.status == 'pending' else "🔄"
            overdue = " 🚨" if task.is_overdue else ""
            
            response += f"{status_icon}{overdue} <b>{task.title}</b>\n"
            response += f"📅 До: {task.due_date.strftime('%d.%m.%Y %H:%M')}\n"
            if task.description:
                # Обрезаем длинное описание
                desc = task.description[:100] + "..." if len(task.description) > 100 else task.description
                response += f"📝 {desc}\n"
            response += "\n"
        
        await message.answer(response, parse_mode='HTML')
        
    except User.DoesNotExist:
        await message.answer(
            "❌ Пользователь не найден.\n\n"
            "Сначала нужно привязать Telegram через команду /start"
        )