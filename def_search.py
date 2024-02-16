import sqlite3

#Функция получает информацию из базы данных
def get_information_from_db(adres):
    with sqlite3.connect('data.db') as connection:
        # Create cursor.
        c = connection.cursor()

        adres = adres.split()
        street = adres[0].capitalize()
        home_number = 'д.' + adres[1].upper()
        adr = ('%' + street + '%' + home_number + '%',)
        sql = "SELECT * FROM data WHERE LOWER(Адрес_дома) LIKE ?"
        c.execute(sql, adr)
        result = c.fetchall()

        if result is None:
            return "Информация о данном адресе не найдена."

        return result


def processing_of_data_for_printing(results):
    if not results:
        return "Данные не найдены"

    processed_results = []

    for result in results:
        # Convert None to "нет данных" and float to int
        result = ["нет данных" if el is None else el for el in result]
        result = [int(el) if isinstance(el, float) else el for el in result]

        # Выбираем более актуальные данные по профилактическим операциям
        if result[19] == 'нет данных':
            result[19], result[20], result[21] = result[22], result[23], result[24]
            if result[22] == 'нет данных':
                result[19], result[20], result[21] = result[25], result[26], result[27]

        keys = ('Адрес', 'Примечание', 'Принадлежность объекта', 'Год постройки', 'Степень огнестойкости', 'Размеры здания',
                'Этажность', 'Количество подъездов(код домофона)', 'Количество квартир', 'Проинструктировано человек',
                'Памятка в п/я', 'Пристрой', 'Тип отопления', 'Вход на чердак снаружи здания (лестница)',
                'Вход на чердак внутри здания (лестница)', 'Доступ под свайное поле', 'Информационный стенд', 'Сухотруб',
                'Ближайший ПВ №', 'Конструктивные элементы', 'Координаты')

        values = (result[0], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[19], result[20],
                  result[21], result[9], result[10], result[11], result[12], result[13], result[14], result[15], result[16],
                  result[17], result[18])

        info_address = dict(zip(keys, values))

        non_output_list = tuple()  # дабвляем ключи елементов словаря info_adres которых не должно быть в выводе

        processed_result = '\n'.join([f'{key}: {value}' for key, value in info_address.items() if key not in non_output_list
                                      and value != 'нет данных'])
        processed_results.append(processed_result)

    return "\n\n".join(processed_results)


def txt_information(adres_home):
    result = get_information_from_db(adres_home)
    return processing_of_data_for_printing(result)




