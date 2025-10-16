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
        [types.KeyboardButton(text="Ретро FM"), types.KeyboardButton(text="Rock FM")],
        [types.KeyboardButton(text="GalnetRadio"), types.KeyboardButton(text="Наше Радио")],
        [types.KeyboardButton(text="Ultra"), types.KeyboardButton(text="Radio Maximum")],
        [types.KeyboardButton(text="Radio Cafe"), types.KeyboardButton(text="Radio Roks")],
        [types.KeyboardButton(text="🔙 Главное меню")]
    ]
    
    await message.answer(
        "🎵 Выберите радиостанцию:",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    )
    await state.set_state(UserStates.music_menu)

# === РАДИОСТАНЦИИ ===
@router.message(StateFilter(UserStates.music_menu), F.text == "Ретро FM")
async def play_retro_fm(message: types.Message):
    radio_url = "http://retroserver.streamr.ru:8043/retro256.mp3"
    await message.answer(f"🎶 Слушаем Ретро FM:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Rock FM")
async def play_energy(message: types.Message):
    radio_url = "https://nashe1.hostingradio.ru/rock-256"
    await message.answer(f"🎶 Слушаем Rock FM:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Galnet") 
async def play_europa_plus(message: types.Message):
    radio_url = "http://galnet.ru:8000/hard"
    await message.answer(f"🎶 Слушаем Galnet Rock:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Наше Радио")
async def play_nashe_radio(message: types.Message):
    radio_url = "http://nashe1.hostingradio.ru:80/nashe-256"
    await message.answer(f"🎶 Слушаем Наше Радио:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Ultra")
async def play_nashe_radio(message: types.Message):
    radio_url = "https://nashe1.hostingradio.ru/ultra-128.mp3"
    await message.answer(f"🎶 Слушаем Радио Ультра:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Radio Maximum")
async def play_nashe_radio(message: types.Message):
    radio_url = "http://maximum.hostingradio.ru/maximum96.aacp"
    await message.answer(f"🎶 Слушаем Radio Maximum:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Radio Cafe")
async def play_nashe_radio(message: types.Message):
    radio_url = "https://on.radio-cafe.ru:6050/stream"
    await message.answer(f"🎶 Слушаем Radio Cafe:\n{radio_url}")

@router.message(StateFilter(UserStates.music_menu), F.text == "Radio Roks")
async def play_nashe_radio(message: types.Message):
    radio_url = "http://icecast.radiorocks.cdnvideo.ru/roks.stream"
    await message.answer(f"🎶 Слушаем Radio Roks:\n{radio_url}")

# === ВОЗВРАТ В ГЛАВНОЕ МЕНЮ ===
@router.message(StateFilter(UserStates.music_menu), F.text == "🔙 Главное меню")
async def back_from_music(message: types.Message, state: FSMContext):
    from bot.handlers.start import show_main_menu
    await state.set_state(UserStates.main_menu)
    await show_main_menu(message)