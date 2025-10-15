import requests
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from django.conf import settings
from bot.states import UserStates

router = Router()

# ==================== КОМАНДА /ask ====================
@router.message(Command("ask"))
async def ask_ai_command(message: types.Message):
    """Обработчик команды /ask"""
    question = message.text.replace('/ask', '').strip()
    
    if not question:
        await message.answer("❌ Напиши вопрос после команды:\n<code>/ask твой вопрос</code>", parse_mode='HTML')
        return
    
    await process_ai_question(message, question)

# ==================== РЕЖИМ AI ====================
@router.message(StateFilter(UserStates.main_menu), F.text == "🤖 Режим AI")
async def enter_ai_mode(message: types.Message, state: FSMContext):
    """Вход в режим AI чата"""
    await state.set_state(UserStates.ai_chat)
    
    keyboard = [
        [types.KeyboardButton(text="🚪 Выйти из режима AI")]
    ]
    
    reply_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    
    await message.answer(
        "🧠 <b>Режим AI активирован!</b>\n\n"
        "Теперь я буду отвечать на все твои сообщения с помощью AI.\n"
        "Просто пиши вопросы - я постараюсь помочь!\n\n"
        "Используй кнопку ниже чтобы выйти из режима.",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

@router.message(StateFilter(UserStates.ai_chat), F.text == "🚪 Выйти из режима AI")
async def exit_ai_mode(message: types.Message, state: FSMContext):
    """Выход из режима AI"""
    from bot.handlers.start import show_main_menu
    await state.set_state(UserStates.main_menu)
    await show_main_menu(message)

@router.message(StateFilter(UserStates.ai_chat), F.text & ~F.text.startswith('/'))
async def handle_ai_chat(message: types.Message):
    """Обработка сообщений в режиме AI"""
    question = message.text
    await process_ai_question(message, question)

# ==================== УМНЫЙ ОПРОС ====================
@router.message(StateFilter(UserStates.main_menu), F.text & ~F.text.startswith('/'))
async def handle_any_message(message: types.Message):
    """Обрабатывает ЛЮБОЕ сообщение в главном меню (кроме команд)"""
    
    # ВАЖНО: Сначала проверяем ВСЕ кнопки меню
    all_menu_buttons = [
        "📋 Мои задачи", "🎮 Режим игры", "🤖 Режим AI", "ℹ️ Помощь",
        "🎵 Музыка", "🌤️ Погода", "💵 Курсы валют"  # ← ВСЕ новые кнопки
    ]
    if message.text in all_menu_buttons:
        return  # ← Пропускаем ВСЕ кнопки меню
    
    # Игнорируем короткие сообщения
    if len(message.text) < 8:
        return
    
    # Проверяем, похоже ли сообщение на вопрос
    question_indicators = ['?', 'что', 'как', 'почему', 'когда', 'где', 'зачем', 'ли', 'объясни', 'расскажи']
    is_question = any(indicator in message.text.lower() for indicator in question_indicators)
    
    if is_question:
        # Спрашиваем хочет ли пользователь ответ от AI
        keyboard = [
            [
                types.InlineKeyboardButton(text="🤖 Да, спросить AI", callback_data=f"ask_ai_{message.message_id}"),
                types.InlineKeyboardButton(text="❌ Нет", callback_data="cancel_ai")
            ]
        ]
        
        await message.answer(
            f"💭 Похоже, ты задал вопрос:\n\n"
            f"«{message.text}»\n\n"
            f"Хочешь чтобы AI помощник ответил на него?",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )

@router.callback_query(F.data.startswith("ask_ai_"))
async def process_ai_request(callback: types.CallbackQuery):
    """Обрабатывает запрос к AI через кнопку"""
    message_id = callback.data.split("_")[2]
    
    # Получаем оригинальное сообщение
    original_message = callback.message.reply_to_message
    if not original_message:
        await callback.answer("Не могу найти оригинальное сообщение")
        return
    
    question = original_message.text
    await process_ai_question(callback.message, question, callback)

@router.callback_query(F.data == "cancel_ai")
async def cancel_ai_request(callback: types.CallbackQuery):
    """Отмена запроса к AI"""
    await callback.message.edit_text("❌ Запрос к AI отменен")
    await callback.answer()

# ==================== ОСНОВНАЯ ЛОГИКА AI ====================
async def process_ai_question(message_or_callback, question, callback=None):
    """Основная функция обработки AI запросов"""
    # Показываем что обрабатываем
    if hasattr(message_or_callback, 'answer'):
        processing_msg = await message_or_callback.answer("🔄 Думаю над ответом...")
    else:
        processing_msg = await message_or_callback.answer("🔄 Думаю над ответом...")
    
    try:
        # Проверяем API ключ
        if not settings.MISTRAL_API_KEY:
            await processing_msg.delete()
            await message_or_callback.answer("❌ API ключ Mistral не настроен")
            return
        
        # Отправляем запрос к Mistral AI
        response = requests.post(
            'https://api.mistral.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {settings.MISTRAL_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'mistral-small-latest',
                'messages': [
                    {
                        'role': 'user', 
                        'content': question
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            },
            timeout=30
        )
        
        # Удаляем сообщение "Думаю..."
        await processing_msg.delete()
        
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            
            # Разбиваем длинные ответы на части
            if len(answer) > 4000:
                parts = [answer[i:i+4000] for i in range(0, len(answer), 4000)]
                for part in parts:
                    await message_or_callback.answer(f"🤖 {part}")
            else:
                await message_or_callback.answer(f"🤖 {answer}")
                
            # Если это callback, убираем кнопки
            if callback:
                await callback.message.edit_reply_markup(reply_markup=None)
                
        else:
            error_msg = f"❌ Ошибка API: {response.status_code}\n"
            if response.status_code == 401:
                error_msg += "Неверный API ключ Mistral"
            elif response.status_code == 429:
                error_msg += "Лимит запросов исчерпан"
            else:
                error_msg += response.text[:500]
                
            await message_or_callback.answer(error_msg)
            
    except requests.exceptions.Timeout:
        await processing_msg.delete()
        await message_or_callback.answer("❌ Превышено время ожидания ответа от AI")
    except Exception as e:
        await processing_msg.delete()
        await message_or_callback.answer(f"❌ Ошибка: {str(e)}")
    
    if callback:
        await callback.answer()