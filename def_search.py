import sqlite3

def search_home(adres):
    try:
        with sqlite3.connect('data.db') as db:

            # Create cursor.
            c = db.cursor()
            # Преобразуем вводимые данные к форматированию в бд.
            adres = adres.split()
            street = adres[0].capitalize()
            home_number = ''.join(adres[1::]).upper().strip()

            # Создаём SQL запрос
            adr = ('%' + street + '%' + home_number + '%',)
            sql = "SELECT * FROM data WHERE Адрес_дома LIKE ?"

            c.execute(sql, adr)
            result = c.fetchone()

            if result is None:
                return "Запрошенный адрес не найден."

            # Convert None to "нет данных" and float to int
            result = ["нет данных" if el is None else el for el in result]
            result = [int(el) if isinstance(el, float) else el for el in result]

            # Выбираем более актуальные данные по профилактическим операциям
            if result[19] == 'нет данных':
                result[19], result[20], result[21] = result[22], result[23], result[24]
                if result[22] == 'нет данных':
                    result[19], result[20], result[21] = result[25], result[26], result[27]

            result = f'''Адрес: {result[0]}
Примечание: {result[2]}
Принадлежность объекта: {result[3]}
Год постройки: {result[4]}
Степень огнестойкости: {result[5]}
Размеры здания, м.: {result[6]}
Этажность: {result[7]}
Количество подъездов(код домофона): {result[8]}
Количество квартир: {result[19]}
Проинструктированно человек: {result[20]}
Памятка в п/я: {result[21]}
Пристрой: {result[9]}
Тип отопления: {result[10]}
Вход на чердак снаружи здания (лестница): {result[11]}
Вход на чердак внутри здания (лестница): {result[12]}
Доступ под свайное поле: {result[13]}
Информационный стенд: {result[14]}
Сухотруб: {result[15]}
Ближайший ПВ №: {result[16]}
Конструктивные элементы: {result[17]}
Координаты: {result[18]}'''
            return result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return "Ощибка подключения к базе данных."
    connect.close()
    return result

