import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, METRO_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_metro_suggestions(query):
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/metro"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {METRO_API_KEY}"
    }
    data = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        suggestions = response.json().get("suggestions", [])
        return [suggestion["value"] for suggestion in suggestions]
    else:
        return []

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот, который может искать станции метро в городе.\n\nНапишите название города на русском языке - например: Москва.")

@dp.message()
async def handle_message(message: Message):
    query = message.text.strip()
    if query:
        suggestions = get_metro_suggestions(query)
        if suggestions:
            response = "Вот несколько станций метро, которые я нашел:\n" + "\n".join(suggestions)
        else:
            response = "Извините, я не смог найти ни одной станции метро, соответствующей вашему запросу."
    else:
        response = "Пожалуйста, отправьте верный запрос."

    await message.answer(response)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())