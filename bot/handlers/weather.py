import requests
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from bot.states import UserStates

router = Router()

@router.message(StateFilter(UserStates.main_menu), F.text == "🌤️ Погода")
async def weather_command(message: types.Message):
    try:
        city = "Новомосковск"
        url = f"http://wttr.in/{city}?format=3"
        response = requests.get(url)
        weather = response.text
        await message.answer(f"🌤️ Погода в {city}:\n{weather}")
    except:
        await message.answer("❌ Не могу получить данные о погоде")