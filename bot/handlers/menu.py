from aiogram import Router, types, F
from aiogram.filters import StateFilter
from bot.states import UserStates
from aiogram.fsm.context import FSMContext

router = Router()

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