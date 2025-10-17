import json
import random
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.states import UserStates

router = Router()

class QuizState(StatesGroup):
    waiting_answer = State()

# Загружаем вопросы из JSON
def load_questions():
    try:
        with open('bot/data/quiz_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['questions']
    except FileNotFoundError:
        # Если файла нет - возвращаем базовые вопросы
        return [
            {
                "question": "Какая столица России?",
                "options": ["Москва", "Питер", "Казань", "Сочи"],
                "answer": "Москва"
            },
            {
                "question": "2 + 2 × 2 = ?", 
                "options": ["6", "8", "4", "10"],
                "answer": "6"
            }
        ]

quiz_questions = load_questions()
user_scores = {}

@router.message(Command("quiz"))
async def start_quiz(message: types.Message, state: FSMContext):
    """Начало викторины"""
    if not quiz_questions:
        await message.answer("❌ Вопросы для викторины не загружены!")
        return
    
    question = random.choice(quiz_questions)
    
    keyboard = []
    for option in question["options"]:
        keyboard.append([types.KeyboardButton(text=option)])
    
    await message.answer(
        f"🧠 <b>Викторина!</b>\n\n{question['question']}",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True),
        parse_mode='HTML'
    )
    
    await state.set_state(QuizState.waiting_answer)
    await state.update_data(current_question=question)

@router.message(QuizState.waiting_answer)
async def check_answer(message: types.Message, state: FSMContext):
    """Проверка ответа"""
    data = await state.get_data()
    question = data["current_question"]
    
    if message.text == question["answer"]:
        user_id = message.from_user.id
        user_scores[user_id] = user_scores.get(user_id, 0) + 1
        await message.answer("✅ <b>Правильно!</b> Отличная работа! 🎉", parse_mode='HTML')
    else:
        await message.answer(f"❌ <b>Неправильно.</b> Правильный ответ: {question['answer']}", parse_mode='HTML')
    
    await state.clear()
    
    # Предложить сыграть еще
    keyboard = [[types.KeyboardButton(text="🎮 Еще викторину")], [types.KeyboardButton(text="🔙 Назад")]]
    await message.answer(
        f"🎯 Сыграем еще? Твой счет: {user_scores.get(message.from_user.id, 0)}",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    )

@router.message(F.text == "🔙 Назад")
async def back_from_quiz(message: types.Message, state: FSMContext):
    from bot.handlers.start import show_main_menu
    await state.set_state(UserStates.main_menu)
    await show_main_menu(message)

@router.message(F.text == "🎮 Еще викторину")
async def another_quiz(message: types.Message, state: FSMContext):
    """Запуск еще одной викторины"""
    await start_quiz(message, state)