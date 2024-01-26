from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import sqlite3


def search_home(adres):

    db = sqlite3.connect('data_home.db')
    #Create cursor.
    c = db.cursor()


    adres = adres.split()
    street = adres[0][0].upper() + adres[0][1::]
    home_number = adres[1]
    adr = ('%' + street + '%' + home_number + '%',)
    sql = "SELECT * FROM data_home WHERE LOWER(Тип) LIKE ?"

    c.execute(sql, adr)
    result = c.fetchall()
    if  result:
        result =f'''Адрес объекта: {result[0][1]} \nПринадлежность: {result[0][2]} \nКоличество квартир: {int(result[0][3])} \nЭтажность: {int(result[0][4])} \nРазмеры в плане, м.: {result[0][5]} \nВысота от уровня земли до конька, м.: {int(result[0][6])} \nСтепень огнестойкости: {int(result[0][7])} \nГод постройки: {int(result[0][8])} \nКоличество жильцов: {result[0][9]} \nОтопление (вид топлива, если печное): {result[0][10]} \nНаличие АПС: {result[0][11]} \nНаличие крана пожаротушения: {result[0][12]} \n'''
        return result

    else:
        result="По запрошенному адресу нет совпадений"
        return result

    db.close()

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '6785402131:AAFzB64VaYufSYp9jQ879vHkWArL2KJhs-A'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        ''
        ''
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    result = search_home(message.text)
    await message.reply(result)


if __name__ == '__main__':
    dp.run_polling(bot)