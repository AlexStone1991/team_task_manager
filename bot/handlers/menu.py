from aiogram import Router, types, F
from aiogram.filters import StateFilter
from bot.states import UserStates

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