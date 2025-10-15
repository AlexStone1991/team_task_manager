from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()
router = Router()

@router.message(Command("tasks"))
async def show_tasks(message: types.Message):
    """Показать задачи пользователя с возможностью завершения"""
    telegram_username = message.from_user.username
    
    try:
        user = await sync_to_async(User.objects.get)(telegram_username=telegram_username)
        
        from tasks.models import Task
        tasks = await sync_to_async(list)(Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress']))
        
        if not tasks:
            await message.answer("✅ У тебя нет активных задач!")
            return
        
        for task in tasks:
            status_icon = "⏳" if task.status == 'pending' else "🔄"
            overdue = " 🚨" if task.is_overdue else ""
            
            # КНОПКА ДЛЯ ЗАВЕРШЕНИЯ ЗАДАЧИ
            keyboard = [[
                types.InlineKeyboardButton(
                    text="✅ Завершить задачу", 
                    callback_data=f"complete_{task.id}"
                )
            ]]
            
            task_text = (
                f"{status_icon}{overdue} <b>{task.title}</b>\n"
                f"📅 До: {task.due_date.strftime('%d.%m.%Y %H:%M')}\n"
            )
            
            if task.description:
                desc = task.description[:100] + "..." if len(task.description) > 100 else task.description
                task_text += f"📝 {desc}\n"
            
            await message.answer(
                task_text,
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard),
                parse_mode='HTML'
            )
            
    except User.DoesNotExist:
        await message.answer("❌ Пользователь не найден.")
@router.callback_query(lambda c: c.data.startswith("complete_"))
async def complete_task(callback: types.CallbackQuery):
    """Завершить задачу через callback"""
    task_id = callback.data.split("_")[1]
    
    try:
        from tasks.models import Task
        task = await sync_to_async(Task.objects.get)(id=task_id)
        task.status = 'completed'
        await sync_to_async(task.save)()
        
        await callback.message.edit_text(
            f"✅ <b>Задача завершена!</b>\n\n"
            f"«{task.title}»\n\n"
            f"Отличная работа! 🎉",
            parse_mode='HTML'
        )
        await callback.answer("Задача отмечена как выполненная!")
        
    except Task.DoesNotExist:
        await callback.answer("Задача не найдена", show_alert=True)