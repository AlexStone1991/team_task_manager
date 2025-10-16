from aiogram import Router, types, F
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()
router = Router()

@router.message(Command("stats"))
async def admin_stats(message: types.Message):
    """Статистика системы для админа"""
    telegram_username = message.from_user.username
    
    try:
        user = await sync_to_async(User.objects.get)(telegram_username=telegram_username)
        
        if not user.is_staff:
            await message.answer("❌ Эта команда только для администраторов")
            return
            
        # Собираем статистику
        total_users = await sync_to_async(User.objects.count)()
        total_tasks = await sync_to_async(Task.objects.count)()
        completed_tasks = await sync_to_async(Task.objects.filter(status='completed').count)()
        pending_tasks = await sync_to_async(Task.objects.filter(status='pending').count)()
        
        # Последние выполненные задачи
        recent_completed = await sync_to_async(list)(
            Task.objects.filter(status='completed').order_by('-created_at')[:5]
        )
        
        stats_text = (
            "📈 <b>Статистика системы</b>\n\n"
            f"👥 Пользователей: {total_users}\n"
            f"📋 Всего задач: {total_tasks}\n"
            f"✅ Выполнено: {completed_tasks}\n"
            f"⏳ Ожидает: {pending_tasks}\n\n"
            "<b>Последние выполненные задачи:</b>\n"
        )
        
        for task in recent_completed:
            # ИСПРАВЛЕНИЕ: используем sync_to_async для связанного поля
            username = await sync_to_async(lambda: task.assigned_to.username)()
            stats_text += f"✅ {task.title} - {username}\n"
            
        await message.answer(stats_text, parse_mode='HTML')
        
    except User.DoesNotExist:
        await message.answer("❌ Пользователь не найден")