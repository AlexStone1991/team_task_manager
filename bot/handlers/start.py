from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from bot.states import UserStates

User = get_user_model()
router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    telegram_username = message.from_user.username
    
    try:
        user = await sync_to_async(User.objects.get)(telegram_username=telegram_username)
        user.telegram_chat_id = message.chat.id
        await sync_to_async(user.save)()
        
        # Сбрасываем состояние в главное меню
        await state.set_state(UserStates.main_menu)
        await show_main_menu(message)
        
    except User.DoesNotExist:
        await message.answer("❌ Пользователь не найден. Обратитесь к администратору.")

async def show_main_menu(message: types.Message):
    """Показать главное меню"""
    keyboard = [
        [types.KeyboardButton(text="📋 Мои задачи")],
        [types.KeyboardButton(text="🎮 Режим игры"), types.KeyboardButton(text="🤖 Режим AI")],
        [types.KeyboardButton(text="🎵 Музыка"), types.KeyboardButton(text="🌤️ Погода")], 
        [types.KeyboardButton(text="🧠 Викторина"), types.KeyboardButton(text="📊 Статистика")],
        [types.KeyboardButton(text="💵 Курсы валют"), types.KeyboardButton(text="ℹ️ Помощь")] 
    ]
    
    reply_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите режим..."
    )
    
    await message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите режим работы:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )