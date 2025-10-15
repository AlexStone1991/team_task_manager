import requests
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from bot.states import UserStates

router = Router()

@router.message(StateFilter(UserStates.main_menu), F.text == "💵 Курсы валют")
async def currency_rates(message: types.Message):
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = response.json()
        
        usd_rate = data['Valute']['USD']['Value']
        eur_rate = data['Valute']['EUR']['Value']
        
        rates = f"""
💵 Курсы валют (ЦБ РФ):
🇺🇸 USD/RUB: {usd_rate:.2f} ₽
🇪🇺 EUR/RUB: {eur_rate:.2f} ₽
        """
        await message.answer(rates)
    except:
        await message.answer("❌ Не могу получить курсы валют")