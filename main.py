from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import sqlite3


def search_home(adres):
    db = sqlite3.connect('data_home.db')
    # Create cursor.
    c = db.cursor()

    adres = adres.split()
    street = adres[0][0].upper() + adres[0][1::]
    home_number = adres[1]
    adr = ('%' + street + '%' + home_number + '%',)
    sql = "SELECT * FROM data_home WHERE LOWER(Тип) LIKE ?"

    c.execute(sql, adr)
    result = c.fetchall()
    result = result[0]

    # меняем типы данных с float на int, убираем None из списка
    result = ["нет данных" if el is None else el for el in result]
    result = [int(el) if isinstance(el, float) else el for el in result]

    if result:
        result = f'''Адрес объекта: {result[1]}
Принадлежность: {result[2]}
Количество квартир: {result[3]}
Этажность: {result[4]}
Размеры в плане, м.: {result[5]}
Высота от уровня земли до конька, м.: {result[6]}
Степень огнестойкости: {result[7]}
Год постройки: {result[8]}
Количество жильцов: {result[9]}
Отопление (вид топлива, если печное): {result[10]}
Наличие АПС: {result[11]}
Наличие крана пожаротушения: {result[12]}'''

        return result

    else:
        result = "По запрошенному адресу нет совпадений"
        return result

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '6785402131:AAFzB64VaYufSYp9jQ879vHkWArL2KJhs-A'

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