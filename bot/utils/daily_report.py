import asyncio
from asgiref.sync import sync_to_async
from django.utils import timezone
from tasks.models import Task
from users.models import User

async def send_daily_reports(bot):  
    """Отправка ежедневных отчетов всем пользователям"""
    users = await sync_to_async(list)(User.objects.filter(telegram_chat_id__isnull=False))
    
    for user in users:
        try:
            # Статистика задач пользователя
            tasks_today = await sync_to_async(list)(
                Task.objects.filter(assigned_to=user, due_date__date=timezone.now().date())
            )
            completed_tasks = await sync_to_async(list)(
                Task.objects.filter(assigned_to=user, status='completed', 
                                  updated_at__date=timezone.now().date())
            )
            
            report = (
                "📊 <b>Ежедневный отчет</b>\n\n"
                f"📅 Задачи на сегодня: {len(tasks_today)}\n"
                f"✅ Выполнено сегодня: {len(completed_tasks)}\n"
                f"🎯 Общий прогресс: отличная работа! 💪"
            )
            
            await bot.send_message(user.telegram_chat_id, report, parse_mode='HTML')
            
        except Exception as e:
            print(f"Ошибка отправки отчета пользователю {user.username}: {e}")

async def start_daily_scheduler(bot):  
    """Запуск ежедневной отправки в 9:00"""
    while True:
        now = timezone.now()
        target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        
        if now > target_time:
            target_time = target_time.replace(day=target_time.day + 1)
        
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        
        await send_daily_reports(bot)  