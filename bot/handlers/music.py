import requests
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from bot.states import UserStates

router = Router()

# === 🎵 МУЗЫКА В ГЛАВНОМ МЕНЮ ===
@router.message(StateFilter(UserStates.main_menu), F.text == "🎵 Музыка")
async def music_menu(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="📻 Ретро FM"), types.KeyboardButton(text="🎸 Rock FM")],
        [types.KeyboardButton(text="🎧 GalnetRadio"), types.KeyboardButton(text="🎵 Наше Радио")],
        [types.KeyboardButton(text="🔙 Главное меню")]
    ]
    
    await message.answer(
        "🎵 Выберите радиостанцию:",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    )
    await state.set_state(UserStates.music_menu)

# === РАДИОСТАНЦИИ ===
# === РАДИОСТАНЦИИ ===
@router.message(StateFilter(UserStates.music_menu), F.text == "📻 Ретро FM")
async def play_retro_fm(message: types.Message):
    await message.answer(
        "🎶 <b>Ретро FM</b>\n\n"
        "Как хотите слушать радио?",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📱 На телефоне", callback_data="radio_phone_retro")],
            [types.InlineKeyboardButton(text="💻 На компьютере", callback_data="radio_pc_retro")],
            [types.InlineKeyboardButton(text="🔗 Просто ссылка", callback_data="radio_link_retro")]
        ]),
        parse_mode='HTML'
    )

@router.message(StateFilter(UserStates.music_menu), F.text == "🎸 Rock FM")
async def play_rock_fm(message: types.Message):
    await message.answer(
        "🎸 <b>Rock FM</b>\n\n"
        "Как хотите слушать радио?",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📱 На телефоне", callback_data="radio_phone_rock")],
            [types.InlineKeyboardButton(text="💻 На компьютере", callback_data="radio_pc_rock")],
            [types.InlineKeyboardButton(text="🔗 Просто ссылка", callback_data="radio_link_rock")]
        ]),
        parse_mode='HTML'
    )

@router.message(StateFilter(UserStates.music_menu), F.text == "🎧 GalnetRadio")
async def play_galnet_radio(message: types.Message): 
    await message.answer(
        "🎧 <b>GalnetRadio</b>\n\n"
        "Как хотите слушать радио?",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📱 На телефоне", callback_data="radio_phone_galnet")],
            [types.InlineKeyboardButton(text="💻 На компьютере", callback_data="radio_pc_galnet")],
            [types.InlineKeyboardButton(text="🔗 Просто ссылка", callback_data="radio_link_galnet")]
        ]),
        parse_mode='HTML'
    )

@router.message(StateFilter(UserStates.music_menu), F.text == "🎵 Наше Радио")
async def play_nashe_radio(message: types.Message):
    await message.answer(
        "🎵 <b>Наше Радио</b>\n\n"
        "Как хотите слушать радио?",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📱 На телефоне", callback_data="radio_phone_nashe")],
            [types.InlineKeyboardButton(text="💻 На компьютере", callback_data="radio_pc_nashe")],
            [types.InlineKeyboardButton(text="🔗 Просто ссылка", callback_data="radio_link_nashe")]
        ]),
        parse_mode='HTML'
    )

# === ОБРАБОТЧИК КНОПОК ВЫБОРА ===
@router.callback_query(F.data.startswith("radio_"))
async def handle_radio_choice(callback: types.CallbackQuery):
    action, station = callback.data.split("_")[1:]
    
    stations = {
        "retro": "http://retro.server101.com/retro_256",  # Ретро FM
        "rock": "https://strm.yandex.ru/cm/rock@341398/master.m3u8",   # Rock FM
        "galnet": "http://galnet.ru:8000/hard", # Galnet
        "nashe": "http://nashe1.hostingradio.ru:80/nashe-256"  # Наше Радио
    }
    
    station_names = {
        "retro": "Ретро FM",
        "rock": "Rock FM", 
        "galnet": "GalnetRadio",
        "nashe": "Наше Радио"
    }
    
    url = stations.get(station, "")
    name = station_names.get(station, "Радиостанция")
    
    if action == "phone":
        text = f"📱 <b>{name} - Для телефона:</b>\n\n{url}\n\n💡 Откройте ссылку в музыкальном приложении"
    elif action == "pc":
        text = f"💻 <b>{name} - Для компьютера:</b>\n\n{url}\n\n💡 Скопируйте ссылку в ваш медиаплеер"
    else:
        text = f"🔗 <b>{name} - Ссылка на радио:</b>\n\n{url}"
    
    await callback.message.edit_text(text, parse_mode='HTML')
    await callback.answer()

# === ВОЗВРАТ В ГЛАВНОЕ МЕНЮ ===
@router.message(StateFilter(UserStates.music_menu), F.text == "🔙 Главное меню")
async def back_from_music(message: types.Message, state: FSMContext):
    from bot.handlers.start import show_main_menu
    await state.set_state(UserStates.main_menu)
    await show_main_menu(message)