from aiogram import Router, types, F
from aiogram.filters import StateFilter
from bot.states import UserStates
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(StateFilter(UserStates.main_menu), F.text == "🔄 Старт")
async def start_button(message: types.Message, state: FSMContext):
    """Перезапуск бота из главного меню"""
    from bot.handlers.start import start_command
    await start_command(message, state)

@router.message(StateFilter(UserStates.main_menu), F.text == "📋 Мои задачи")
async def show_tasks_button(message: types.Message):
    """Показать задачи из главного меню"""
    from bot.handlers.tasks import show_tasks
    await show_tasks(message)

@router.message(StateFilter(UserStates.main_menu), F.text == "ℹ️ Помощь")
async def help_button(message: types.Message):
    """Показать помощь из главного меню"""
    from bot.handlers.help import help_command
    await help_command(message)

@router.message(StateFilter(UserStates.main_menu), F.text == "🧠 Викторина")
async def quiz_button(message: types.Message, state: FSMContext):
    """Запуск викторины из главного меню"""
    from bot.handlers.quiz import start_quiz
    await start_quiz(message, state)

@router.message(StateFilter(UserStates.main_menu), F.text == "📊 Статистика")
async def stats_button(message: types.Message):
    """Показать статистику из главного меню"""
    from bot.handlers.admin_stats import admin_stats
    await admin_stats(message)

# ==================== ОБРАБОТЧИКИ ДЛЯ ГОСТЕВОГО РЕЖИМА ====================
@router.message(StateFilter(UserStates.guest_mode), F.text == "🔄 Старт")
async def guest_start(message: types.Message, state: FSMContext):
    """Перезапуск для гостей"""
    from bot.handlers.start import start_command
    await start_command(message, state)

@router.message(StateFilter(UserStates.guest_mode), F.text == "🎮 Режим игры")
async def guest_game_mode(message: types.Message, state: FSMContext):
    """Игровой режим для гостей"""
    from bot.handlers.games import show_game_menu
    await state.set_state(UserStates.game_mode)
    await show_game_menu(message)

@router.message(StateFilter(UserStates.guest_mode), F.text == "🎵 Музыка")
async def guest_music(message: types.Message):
    """Музыка для гостей"""
    from bot.handlers.music import music_command
    await music_command(message)

@router.message(StateFilter(UserStates.guest_mode), F.text == "🌤️ Погода")
async def guest_weather(message: types.Message):
    """Погода для гостей"""
    from bot.handlers.weather import weather_command
    await weather_command(message)

@router.message(StateFilter(UserStates.guest_mode), F.text == "🧠 Викторина")
async def guest_quiz(message: types.Message, state: FSMContext):
    """Викторина для гостей"""
    from bot.handlers.quiz import start_quiz
    await start_quiz(message, state)

@router.message(StateFilter(UserStates.guest_mode), F.text == "💵 Курсы валют")
async def guest_currency(message: types.Message):
    """Курсы валют для гостей"""
    from bot.handlers.currency import currency_command
    await currency_command(message)

@router.message(StateFilter(UserStates.guest_mode), F.text == "ℹ️ Помощь")
async def guest_help(message: types.Message):
    """Помощь для гостей"""
    from bot.handlers.help import help_command
    await help_command(message)

@router.message(StateFilter(UserStates.guest_mode), F.text == "🔄 Старт")
async def guest_start(message: types.Message, state: FSMContext):
    """Перезапуск для гостей"""
    from bot.handlers.start import start_command
    await start_command(message, state)