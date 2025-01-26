import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, METRO_API_KEY

DADATA_URL = "https://dadata.ru/api/v2/suggest/metro"

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def fetch_metro_stations(query: str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {METRO_API_KEY}"
    }
    data = {
        "query": query
    }
    response = requests.post(DADATA_URL, json=data, headers=headers)
    return response.json()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет! Введите название станции метро, чтобы получить информацию.")


@dp.message()
async def handle_message(message: Message):
    query = message.text
    result = await asyncio.to_thread(fetch_metro_stations, query)

    if "suggestions" in result and result["suggestions"]:
        response_text = "\n".join(
            f"{suggestion['value']} ({suggestion['data']['city']})"
            for suggestion in result["suggestions"]
        )
    else:
        response_text = "Станции не найдены."

    await message.reply(response_text)


async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())