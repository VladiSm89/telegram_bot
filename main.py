from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from def_search import search_home
from config import BOT_TOKEN


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('''Это телеграм-бот информирует о характеристиках объекта.
Для получения информации напиши ему название улицы и номер строения.
Запрос писать в виде: "НАЗВАНИЕ УЛИЦЫ" "НОМЕР СТРОЕНИЯ". 
Пишем название улицы и номер дома через пробел. ''')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('''Это телеграм-бот информирует о характеристиках объекта.
Для получения информации напиши ему название улицы и номер строения.
Запрос писать в виде: "НАЗВАНИЕ УЛИЦЫ" "НОМЕР СТРОЕНИЯ". 
Пишем название улицы и номер дома через пробел. ''')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    result = search_home(message.text)
    await message.reply(result)


if __name__ == '__main__':
    dp.run_polling(bot)