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
        # Ищем пользователя в БД Django
        user = await sync_to_async(User.objects.get)(telegram_username=telegram_username)
        user.telegram_chat_id = message.chat.id
        await sync_to_async(user.save)()
        
        # ПОЛНОЦЕННЫЙ РЕЖИМ
        await state.set_state(UserStates.main_menu)
        await message.answer(
            "✅ <b>Добро пожаловать!</b>\n\n"
            "Вы авторизованы и можете пользоваться всеми функциями бота!",
            parse_mode='HTML'
        )
        await show_main_menu(message)
        
    except User.DoesNotExist:
        # ГОСТЕВОЙ РЕЖИМ
        await state.set_state(UserStates.guest_mode)
        await message.answer(
            "👋 <b>Гостевой режим</b>\n\n"
            "🎮 <b>Доступные функции:</b>\n"
            "• Все игры (камень-ножницы-бумага, виселица, крестики-нолики)\n"
            "• Музыка, погода, курсы валют\n"
            "• Викторина и справка\n\n"
            "🔒 <b>Недоступно:</b>\n"
            "• Работа с задачами\n"
            "• Статистика\n\n"
            "💡 <b>Для полного доступа:</b>\n"
            "Зарегистрируйтесь на сайте: http://127.0.0.1:8000/",
            parse_mode='HTML'
        )
        await show_guest_menu(message)

async def show_main_menu(message: types.Message):
    """Главное меню для авторизованных пользователей"""
    keyboard = [
        [types.KeyboardButton(text="🔄 Старт")],
        [types.KeyboardButton(text="📋 Мои задачи")],
        [types.KeyboardButton(text="🎮 Режим игры"), types.KeyboardButton(text="🤖 Режим AI")],
        [types.KeyboardButton(text="🎵 Музыка"), types.KeyboardButton(text="🌤️ Погода")], 
        [types.KeyboardButton(text="🧠 Викторина"), types.KeyboardButton(text="📊 Статистика")],
        [types.KeyboardButton(text="💵 Курсы валют"), types.KeyboardButton(text="ℹ️ Помощь")],
        
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

async def show_guest_menu(message: types.Message):
    """Меню для гостевого режима"""
    keyboard = [
        [types.KeyboardButton(text="🎮 Режим игры")],
        [types.KeyboardButton(text="🎵 Музыка"), types.KeyboardButton(text="🌤️ Погода")],
        [types.KeyboardButton(text="🧠 Викторина"), types.KeyboardButton(text="💵 Курсы валют")],
        [types.KeyboardButton(text="ℹ️ Помощь"), types.KeyboardButton(text="🔄 Старт")]
    ]
    
    reply_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите функцию..."
    )
    
    await message.answer(
        "👋 <b>Гостевой режим</b>\n\n"
        "Выберите функцию:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )