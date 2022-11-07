import sqlite3
import test
import coingecko
import keyboards
from config import DATA


def create_table(event):
    connection = sqlite3.connect(DATA)
    sqlite_create_table = f'''CREATE TABLE IF NOT EXISTS {event.chat.first_name}_{event.chat.id} (
        id TEXT PRIMARY KEY,
        name TEXT, 
        value  REAL DEFAULT (0),
        price  REAL DEFAULT (0) 
    );'''
    cursor = connection.cursor()
    cursor.execute(sqlite_create_table)
    connection.commit()

    cursor.close()


def insert_to_table(coin_list, message):
    id_coin = coin_list[0]
    name = coin_list[1]
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_insert_table = f'''INSERT INTO {message.chat.first_name}_{message.chat.id} (
                                        id, name)
                                        VALUES
                                        ('{id_coin}', '{name}');'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_insert_table)
    sqlite_connection.commit()

    cursor.close()


def select_id(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name, value, price FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []
    for k in all_results:
        coin_list += k
    return coingecko.portfolio(coin_list)


def add_value(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []
    for k in all_results:
        coin_list += k
    return keyboards.inline_keyboards(coin_list)


def select_value_coin(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id FROM {content.from_user.first_name}_{content.from_user.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()
    sqlite_connection.commit()
    cursor.close()

    coin_list = []
    for k in all_results:
        coin_list += k
    return coin_list


def add_value_coin(content, data):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_add_value = f'''UPDATE {content.from_user.first_name}_{content.from_user.id} 
    SET value = {content.text} WHERE id = '{data[::-6]}';'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_add_value)

    sqlite_connection.commit()
    cursor.close()


def drop_table(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_create_table_query = f'''DROP TABLE {content.chat.first_name}_{content.chat.id};'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()

    cursor.close()


def delete_coin(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []
    for k in all_results:
        coin_list += k
    return keyboards.inline_keyboard_del(coin_list)


def del_coin(content, data):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_delete = f'''DELETE FROM {data.chat.first_name}_{data.chat.id} 
        WHERE id = '{content[0:-4]}';'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_delete)

    sqlite_connection.commit()
    cursor.close()


def delete_coin_id(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []
    del_coin_list = list()
    for k in all_results:
        coin_list += k
    coin_data = [coins for coins in coin_list[::2]]
    for i in coin_data:
        item_del = i + '_del'
        del_coin_list.append(item_del)
    return del_coin_list


def status_keyboard(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []

    for k in all_results:
        coin_list += k
    return keyboards.inline_keyboard_stat(coin_list)


def add_value_price(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []
    for k in all_results:
        coin_list += k
    return keyboards.inline_add_price(coin_list)


def select_price_coin(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id FROM {content.from_user.first_name}_{content.from_user.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()
    sqlite_connection.commit()
    cursor.close()

    coin_list = []
    price_coin_list = list()
    for k in all_results:
        coin_list += k
    for i in coin_list:
        item_del = i + '_price'
        price_coin_list.append(item_del)
    return price_coin_list


def add_price(content, data):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_add_value = f'''UPDATE {content.from_user.first_name}_{content.from_user.id} 
    SET price = {content.text} WHERE id = '{data[0:-6]}';'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_add_value)

    sqlite_connection.commit()
    cursor.close()


def add_transact(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id, name FROM {content.chat.first_name}_{content.chat.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()

    sqlite_connection.commit()
    cursor.close()
    coin_list = []
    for k in all_results:
        coin_list += k
    return keyboards.inline_add_transaction(coin_list)


def select_transact(content):
    sqlite_connection = sqlite3.connect(DATA)
    sqlite_select = f'''SELECT id FROM {content.from_user.first_name}_{content.from_user.id} ;'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_select)
    all_results = cursor.fetchall()
    sqlite_connection.commit()
    cursor.close()

    coin_list = []
    price_coin_list = list()
    for k in all_results:
        coin_list += k
    for i in coin_list:
        item_del = i + '_tarns'
        price_coin_list.append(item_del)
    return price_coin_list


def transaction(coin_data):
    sqlite_connection = sqlite3.connect(DATA)
    cursor = sqlite_connection.cursor()
    cursor.execute(f'SELECT * FROM {coin_data[0]} WHERE id == ?;', (coin_data[1],))
    coin_data_old = cursor.fetchall()
    value = (coin_data[2])
    price = (coin_data[3])
    value_old = (coin_data_old[0][2])
    price_old = (coin_data_old[0][3])
    if price_old == 0 or value_old == 0:
        cursor.execute(f'''UPDATE {coin_data[0]} SET price = {price}, value = {value}
            WHERE id = '{coin_data[1]}';''')
        sqlite_connection.commit()
        cursor.close()
        return price
    else:
        cost_by = value * price + value_old * price_old
        all_value = value + value_old
        aver_price = cost_by / all_value
        all_coin = value + value_old
        cursor.execute(f'''UPDATE {coin_data[0]} SET price = {aver_price}, value = {all_coin}
        WHERE id = '{coin_data[1]}';''')
        sqlite_connection.commit()
        cursor.close()
        if aver_price > 1:
            aver_price = round(aver_price, 1)
        else:
            aver_price = round(aver_price, 5)
        return aver_price

