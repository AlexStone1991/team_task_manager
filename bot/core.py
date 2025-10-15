import os
import django
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Настраиваем Django ДО всего
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from bot.handlers.start import router as start_router
from bot.handlers.tasks import router as tasks_router
from bot.handlers.help import router as help_router
from bot.handlers.games import router as games_router
from bot.handlers.music import router as music_router  # ← ДОБАВЬ
from bot.handlers.weather import router as weather_router  # ← ДОБАВЬ
from bot.handlers.currency import router as currency_router  # ← ДОБАВЬ
from bot.handlers.menu import router as menu_router
from bot.handlers.ai_chat import router as ai_chat_router


async def main():
    """Главная функция бота"""
    print("🤖 Запускаем бота...")
    
    # Проверяем токен
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        print("❌ ОШИБКА: TELEGRAM_BOT_TOKEN не найден в .env файле!")
        return
    
    # Создаем бота
    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(tasks_router)
    dp.include_router(help_router)
    dp.include_router(games_router)
    dp.include_router(music_router)  # ← ДОБАВЬ
    dp.include_router(weather_router)  # ← ДОБАВЬ
    dp.include_router(currency_router)  # ← ДОБАВЬ
    dp.include_router(menu_router)
    dp.include_router(ai_chat_router)
    
    print("🚀 Бот запущен")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())