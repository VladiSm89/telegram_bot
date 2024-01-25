from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import sqlite3
from fuzzywuzzy import fuzz

def search_home(search_input):
    db = sqlite3.connect('data_home.db')
    c = db.cursor()

    c.execute("SELECT * FROM data_home")
    all_rows = c.fetchall()

    max_similarity = 0
    best_match = None

    search_input = search_input.split()
    search_street = search_input[0].capitalize()
    search_home_number = search_input[1]

    for row in all_rows:
        db_street = row[1].lower()  # Assuming street is in the second column, adjust if needed
        db_home_number = row[2]  # Assuming home number is in the third column, adjust if needed

        street_similarity = fuzz.partial_ratio(search_street.lower(), db_street)
        home_number_similarity = fuzz.partial_ratio(search_home_number, str(db_home_number))

        total_similarity = (street_similarity + home_number_similarity) / 2

        if total_similarity > max_similarity:
            max_similarity = total_similarity
            best_match = row

    if best_match:
        result_string = f"Наиболее подходящий результат: {', '.join(map(str, best_match))}"
        return result_string
    else:
        result_string = "По запрошенному адресу нет совпадений"
        return result_string




    db.close()

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '6785402131:AAFzB64VaYufSYp9jQ879vHkWArL2KJhs-A'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    result = search_home(message.text)
    await message.reply(result)


if __name__ == '__main__':
    dp.run_polling(bot)