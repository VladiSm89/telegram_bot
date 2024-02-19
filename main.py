from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from def_search import txt_information

import pandas as pd
import sqlite3
from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def process_excel(message: Message):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    # Преобразование файла Excel в базу данных SQLite
    df = pd.read_excel(downloaded_file)
    conn = sqlite3.connect('data.db')
    df.to_sql('data', conn, index=False, if_exists='replace')
    conn.close()

    # Сообщение об успешном обновлении базы данных
    await message.answer("База данных успешно обновлена!")


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


@dp.message(Command(commands=['bdupdate']))
async def bdupdate_handler(message: Message):
    if message.document:
        await process_excel(message)
    else:
        await message.answer("Пожалуйста, пришлите файл Excel для обновления базы данных.")


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(txt_information(message.text))


if __name__ == '__main__':
    dp.run_polling(bot)