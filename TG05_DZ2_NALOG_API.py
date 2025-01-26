import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, NALOG_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_nalog_suggestions(query):
    url = "http://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/fns_unit"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {NALOG_API_KEY}"
    }
    data = {
     'query': query,  # Идентификатор организации
     'fields': ['codeinn']  # Поле, по которому производится поиск
}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        suggestions = response.json().get("suggestions", [])
        return [suggestion["value"] for suggestion in suggestions] # Возвращает список значений
    else:
        return []

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот, который может искать инспекции ФНС.\n\nНапишите четырехзначный код, например: 5401 ")

@dp.message()
async def handle_message(message: Message):
    query = message.text.strip()
    if query:
        suggestions = get_nalog_suggestions(query)
        if suggestions:
            response = "Вот, что я нашел по Вашему запросу:\n" + "\n".join(suggestions)
        else:
            response = "Извините, я не смог найти данные, соответствующей вашему запросу."
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
