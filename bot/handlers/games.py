from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states import UserStates
import random

router = Router()
ROCK = "Камень"
SCISSORS = "Ножницы"
PAPER = "Бумага"

@router.message(F.text == "🎮 Режим игры")
async def enter_game_mode(message: types.Message, state: FSMContext):
    """Вход в режим игры"""
    await state.set_state(UserStates.game_mode)
    
    keyboard = [
        [types.KeyboardButton(text="🎮 Играть")],
        [types.KeyboardButton(text="🚪 Выйти из игрового режима")]
    ]
    
    reply_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    
    await message.answer(
        "🎯 <b>Игровой режим активирован!</b>\n\n"
        "Нажми '🎮 Играть' чтобы начать игру в камень-ножницы-бумага!\n\n"
        "Используй кнопку ниже чтобы выйти из режима.",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

@router.message(StateFilter(UserStates.game_mode), F.text == "🚪 Выйти из игрового режима")
async def exit_game_mode(message: types.Message, state: FSMContext):
    """Выход из игрового режима"""
    from bot.handlers.start import show_main_menu
    await state.set_state(UserStates.main_menu)
    await show_main_menu(message)

@router.message(StateFilter(UserStates.game_mode), F.text == "🎮 Играть")
async def game_in_mode(message: types.Message):
    """Запуск игры в игровом режиме"""
    await game_command(message)

# Остальной код игры остается без изменений
@router.message(Command("game"))
async def game_command(message: types.Message):
    """Запуск игры в камень-ножницы-бумага"""

    keyboard = [
        [types.InlineKeyboardButton(text="✊ Камень", callback_data=ROCK)],
        [types.InlineKeyboardButton(text="✌️ Ножницы", callback_data=SCISSORS)],
        [types.InlineKeyboardButton(text="✋ Бумага", callback_data=PAPER)]
    ]
    
    await message.answer(
        "🎮 <b>Камень-Ножницы-Бумага!</b>\n\nВыбери свой ход:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode='HTML'
    )

@router.callback_query(F.data.in_([ROCK, SCISSORS, PAPER]))
async def process_game(callback: types.CallbackQuery):
    user_choice = callback.data
    bot_choice = random.choice([ROCK, SCISSORS, PAPER])
    
    choices = {ROCK: "✊", SCISSORS: "✌️", PAPER: "✋"}
    
    if user_choice == bot_choice:
        result = "🤝 <b>Ничья!</b>"
    elif (user_choice == ROCK and bot_choice == SCISSORS) or \
         (user_choice == SCISSORS and bot_choice == PAPER) or \
         (user_choice == PAPER and bot_choice == ROCK):
        result = "🎉 <b>Ты выиграл!</b>"
    else:
        result = "😎 <b>Я выиграл!</b>"
    
    await callback.message.edit_text(
        f"🎮 <b>Результат игры:</b>\n\n"
        f"Ты: {choices[user_choice]} {user_choice}\n"
        f"Бот: {choices[bot_choice]} {bot_choice}\n\n"
        f"{result}\n\n"
        f"Хочешь сыграть еще? Нажми '🎮 Играть'",
        parse_mode='HTML'
    )
    await callback.answer()