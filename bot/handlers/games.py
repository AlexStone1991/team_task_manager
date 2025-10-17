from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states import UserStates
import random

router = Router()

# ==================== КАМЕНЬ-НОЖНИЦЫ-БУМАГА (твой рабочий код) ====================
ROCK = "Камень"
SCISSORS = "Ножницы"
PAPER = "Бумага"

async def show_game_menu(message: types.Message):
    """Показать меню игр"""
    keyboard = [
        [types.KeyboardButton(text="🎮 Камень-ножницы-бумага")],
        [ types.KeyboardButton(text="🎭 Виселица"), types.KeyboardButton(text="❌⭕ Крестики-нолики")],
        [types.KeyboardButton(text="🚪 Выйти из игрового режима")]
    ]
    
    await message.answer(
        "🎮 <b>ИГРОВОЙ РЕЖИМ</b>\n\nВыбери игру:",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True),
        parse_mode='HTML'
    )

@router.message(StateFilter(UserStates.main_menu), F.text == "🎮 Режим игры")
async def enter_game_mode(message: types.Message, state: FSMContext):
    """Вход в режим игры"""
    await state.set_state(UserStates.game_mode)
    await show_game_menu(message)

@router.message(StateFilter(UserStates.game_mode), F.text == "🚪 Выйти из игрового режима")
async def exit_game_mode(message: types.Message, state: FSMContext):
    """Выход из игрового режима"""
    from bot.handlers.start import show_main_menu
    await state.set_state(UserStates.main_menu)
    await show_main_menu(message)

@router.message(StateFilter(UserStates.game_mode), F.text == "🎮 Камень-ножницы-бумага")
async def play_rps_in_mode(message: types.Message):
    """Запуск камень-ножницы-бумага из меню игр"""
    await game_command(message)

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
        f"Хочешь сыграть еще? Вернись в игровой режим!",
        parse_mode='HTML'
    )
    await callback.answer()

# ==================== КРЕСТИКИ-НОЛИКИ (ПЕРЕПИСАННЫЕ БЕЗ FSM) ====================

# Глобальный словарь для хранения игр (как в твоей рабочей логике)
tic_tac_toe_games = {}

@router.message(StateFilter(UserStates.game_mode), F.text == "❌⭕ Крестики-нолики")
async def start_tic_tac_toe(message: types.Message):
    """Начало игры в крестики-нолики"""
    user_id = message.from_user.id
    
    # Создаем новую доску
    board = [[" " for _ in range(3)] for _ in range(3)]
    
    # Сохраняем игру
    tic_tac_toe_games[user_id] = {
        'board': board,
        'player_turn': True
    }
    
    # Создаем клавиатуру
    keyboard = create_tic_tac_toe_keyboard(board)
    
    await message.answer(
        "❌⭕ <b>Крестики-нолики!</b>\n\n"
        "Ты играешь крестиками (❌). Выбери клетку:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data.startswith("ttt_"))
async def process_tic_tac_toe_move(callback: types.CallbackQuery):
    """Обработка хода в крестики-нолики"""
    user_id = callback.from_user.id
    
    # Выход из игры
    if callback.data == "ttt_exit":
        if user_id in tic_tac_toe_games:
            del tic_tac_toe_games[user_id]
        await callback.message.edit_text("🚪 Вышел из игры в крестики-нолики")
        await callback.answer()
        return
    
    # Проверяем, есть ли активная игра
    if user_id not in tic_tac_toe_games:
        await callback.answer("Игра не найдена! Начни заново.")
        return
    
    game = tic_tac_toe_games[user_id]
    board = game['board']
    
    # Проверяем, чей сейчас ход
    if not game['player_turn']:
        await callback.answer("Сейчас не твой ход!")
        return
    
    # Получаем координаты
    try:
        row, col = map(int, callback.data.replace("ttt_", "").split("_"))
    except:
        await callback.answer("Ошибка координат!")
        return
    
    # Проверяем, свободна ли клетка
    if board[row][col] != " ":
        await callback.answer("Эта клетка уже занята!")
        return
    
    # Ход игрока
    board[row][col] = "X"
    
    # Проверка победы игрока
    if check_win(board, "X"):
        keyboard = create_tic_tac_toe_keyboard(board)
        await callback.message.edit_text(
            "🎉 <b>Ты выиграл! Поздравляю!</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        del tic_tac_toe_games[user_id]
        await callback.answer()
        return
    
    # Проверка ничьи
    if is_board_full(board):
        keyboard = create_tic_tac_toe_keyboard(board)
        await callback.message.edit_text(
            "🤝 <b>Ничья! Игра завершена.</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        del tic_tac_toe_games[user_id]
        await callback.answer()
        return
    
    # Ход бота
    bot_row, bot_col = find_best_move(board)
    if bot_row != -1:
        board[bot_row][bot_col] = "O"
        
        # Проверка победы бота
        if check_win(board, "O"):
            keyboard = create_tic_tac_toe_keyboard(board)
            await callback.message.edit_text(
                "😎 <b>Я выиграл! Попробуй еще раз!</b>",
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            del tic_tac_toe_games[user_id]
            await callback.answer()
            return
        
        # Проверка ничьи после хода бота
        if is_board_full(board):
            keyboard = create_tic_tac_toe_keyboard(board)
            await callback.message.edit_text(
                "🤝 <b>Ничья! Игра завершена.</b>",
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            del tic_tac_toe_games[user_id]
            await callback.answer()
            return
    
    # Обновляем состояние игры
    game['player_turn'] = True
    
    # Обновляем клавиатуру
    keyboard = create_tic_tac_toe_keyboard(board)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

def create_tic_tac_toe_keyboard(board):
    """Создание клавиатуры для крестиков-ноликов"""
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            if board[i][j] == "X":
                text = "❌"
            elif board[i][j] == "O":
                text = "⭕"
            else:
                text = "⬜️"
            row.append(types.InlineKeyboardButton(text=text, callback_data=f"ttt_{i}_{j}"))
        keyboard.append(row)
    
    keyboard.append([types.InlineKeyboardButton(text="🚪 Выйти из игры", callback_data="ttt_exit")])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

def check_win(board, player):
    """Проверка победы"""
    # Проверка строк
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
    
    # Проверка столбцов
    for j in range(3):
        if all(board[i][j] == player for i in range(3)):
            return True
    
    # Проверка диагоналей
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    
    return False

def find_best_move(board):
    """Поиск лучшего хода для бота"""
    # Сначала проверяем выигрышные ходы
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if check_win(board, "O"):
                    return i, j
                board[i][j] = " "
    
    # Блокируем выигрышные ходы игрока
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                if check_win(board, "X"):
                    return i, j
                board[i][j] = " "
    
    # Центр
    if board[1][1] == " ":
        return 1, 1
    
    # Углы
    corners = [(0,0), (0,2), (2,0), (2,2)]
    random.shuffle(corners)
    for i, j in corners:
        if board[i][j] == " ":
            return i, j
    
    # Случайный ход
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells) if empty_cells else (-1, -1)

def is_board_full(board):
    """Проверка заполненности доски"""
    return all(board[i][j] != " " for i in range(3) for j in range(3))


# ==================== ВИСЕЛИЦА (С ПОДСКАЗКАМИ) ====================
hangman_games = {}
hangman_words = {
    "ПИТОН": "🐍 Язык программирования",
    "ПРОГРАММИРОВАНИЕ": "💻 Создание программ", 
    "ТЕЛЕГРАМ": "📱 Мессенджер",
    "БОТ": "🤖 Автоматизированная программа",
    "КОМПЬЮТЕР": "🖥️ Электронное устройство",
    "АЛГОРИТМ": "📊 Последовательность действий",
    "ПРОГРАММА": "⚙️ Набор инструкций",
    "ФУНКЦИЯ": "🔧 Блок кода",
    "ПЕРЕМЕННАЯ": "📦 Хранилище данных"
}

@router.message(StateFilter(UserStates.game_mode), F.text == "🎭 Виселица")
async def start_hangman(message: types.Message):
    """Начало игры 'Виселица'"""
    user_id = message.from_user.id
    word, hint = random.choice(list(hangman_words.items()))
    hidden_word = ["_" for _ in word]
    attempts = 6
    
    hangman_games[user_id] = {
        'word': word,
        'hint': hint,
        'hidden_word': hidden_word,
        'attempts': attempts,
        'used_letters': set()
    }
    
    # Создаем клавиатуру с буквами
    keyboard = []
    row = []
    letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    
    for letter in letters:
        row.append(types.InlineKeyboardButton(text=letter, callback_data=f"hangman_{letter}"))
        if len(row) == 6:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([types.InlineKeyboardButton(text="🚪 Выйти из игры", callback_data="hangman_exit")])
    
    hangman_figure = get_hangman_figure(attempts)
    
    text = f"🎭 <b>Виселица!</b>\n\n{hangman_figure}\n\n"
    text += f"💡 <b>Подсказка:</b> {hint}\n\n"
    text += f"Слово: {' '.join(hidden_word)}\n"
    text += f"Букв в слове: {len(word)}\n"
    text += f"Осталось попыток: {attempts}\n\n"
    text += "Выбери букву:"
    
    # Отправляем новое сообщение с inline-клавиатурой
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode='HTML')

def get_hangman_figure(attempts):
    """Получить фигуру виселицы"""
    figures = [
        """
        ┌───
        │  🙂
        │ /|\\
        │ / \\
        │
        """,
        """
        ┌───
        │  😐
        │ /|\\
        │ / 
        │
        """,
        """
        ┌───
        │  😐
        │ /|
        │ / 
        │
        """,
        """
        ┌───
        │  😐
        │  |
        │ / 
        │
        """,
        """
        ┌───
        │  😐
        │  |
        │  
        │
        """,
        """
        ┌───
        │  😟
        │  
        │  
        │
        """,
        """
        ┌───
        │  
        │  
        │  
        │
        """
    ]
    return figures[6 - attempts]

@router.callback_query(F.data.startswith("hangman_"))
async def process_hangman_letter(callback: types.CallbackQuery):
    """Обработка выбора буквы в виселице"""
    user_id = callback.from_user.id
    
    if callback.data == "hangman_exit":
        if user_id in hangman_games:
            del hangman_games[user_id]
        await callback.message.edit_text("🚪 Вышел из игры 'Виселица'")
        await callback.answer()
        return
    
    if user_id not in hangman_games:
        await callback.answer("Игра не найдена! Начни заново.")
        return
    
    letter = callback.data.replace("hangman_", "")
    game = hangman_games[user_id]
    word = game['word']
    hint = game['hint']
    hidden_word = game['hidden_word']
    attempts = game['attempts']
    used_letters = game['used_letters']
    
    if letter in used_letters:
        await callback.answer("Эта буква уже использована!")
        return
    
    used_letters.add(letter)
    
    if letter in word:
        # Открываем угаданные буквы
        for i, char in enumerate(word):
            if char == letter:
                hidden_word[i] = letter
        message_text = f"✅ Буква '{letter}' есть в слове!"
    else:
        attempts -= 1
        game['attempts'] = attempts
        message_text = f"❌ Буквы '{letter}' нет в слове!"
    
    # Проверяем условия окончания игры
    if "_" not in hidden_word:
        await callback.message.edit_text(
            f"🎉 <b>Поздравляю! Ты угадал слово: {word}</b>\n\n"
            f"💡 Подсказка была: {hint}",
            parse_mode='HTML'
        )
        del hangman_games[user_id]
        await callback.answer()
        return
    
    if attempts <= 0:
        await callback.message.edit_text(
            f"💀 <b>Игра окончена! Загаданное слово: {word}</b>\n\n"
            f"💡 Подсказка была: {hint}\n\n"
            f"{get_hangman_figure(0)}",
            parse_mode='HTML'
        )
        del hangman_games[user_id]
        await callback.answer()
        return
    
    # Обновляем клавиатуру
    keyboard = []
    row = []
    letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    
    for l in letters:
        if l in used_letters:
            if l in word:
                text = f"✅{l}"
            else:
                text = f"❌{l}"
            row.append(types.InlineKeyboardButton(text=text, callback_data="hangman_used"))
        else:
            row.append(types.InlineKeyboardButton(text=l, callback_data=f"hangman_{l}"))
        
        if len(row) == 6:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([types.InlineKeyboardButton(text="🚪 Выйти из игры", callback_data="hangman_exit")])
    
    hangman_figure = get_hangman_figure(attempts)
    
    text = f"🎭 <b>Виселица!</b>\n\n{hangman_figure}\n\n"
    text += f"💡 <b>Подсказка:</b> {hint}\n\n"
    text += f"Слово: {' '.join(hidden_word)}\n"
    text += f"Осталось попыток: {attempts}\n"
    text += f"Использованные буквы: {', '.join(sorted(used_letters))}\n\n"
    text += f"{message_text}\n\n"
    text += "Выбери букву:"
    
    # Редактируем существующее сообщение
    await callback.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode='HTML')
    await callback.answer()