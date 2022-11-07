import etherscan
import text_write
import database
from config import *
from keyboards import *
from buttons import Buttons
from database import *

con = sqlite3.connect(DATA, check_same_thread=False)
bot = telebot.TeleBot(TOKEN)

bt = Buttons()


# Старт бота та головне меню
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Головне меню", reply_markup=main)


# Реагує на кнопку 📊 Інфо про монети
@bot.message_handler(func=lambda message: message.text == bt.info)
def info(message):
    msg = bot.send_message(message.chat.id, "Введи маркер монети наприклад BTC",
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, congeko_info)


# Повторний запит якщо користувач ввів не вірний символ
def repeat_request(message):
    try:
        bot.send_message(message.chat.id, coingecko.get_token_price(message.text), reply_markup=main)
    except Exception:
        msg = bot.send_message(message.chat.id, """Упс такої монети не знайдено 🤷‍♂
Спробуй ще раз""", reply_markup=keyboards.back_to_menu)
        bot.register_next_step_handler(msg, repeat_request)


# Виводит результат запиту
def congeko_info(message):
    try:
        bot.send_message(message.chat.id, coingecko.get_token_price(message.text), reply_markup=main)
    except IndexError:
        msg = bot.send_message(message.chat.id, """Упс такої монети не знайдено 🤷‍♂
Спробуй ще раз""")
        bot.register_next_step_handler(msg, repeat_request)


# Реагує на кнопку 💸 Підтримка проекту
@bot.message_handler(func=lambda message: message.text == bt.support)
def support_project(message):
    bot.send_message(message.chat.id, 'Тут можна поділитись ідеями та підтримати монетами',
                     reply_markup=support)


# Реагує на кнопку 📨 Скарги та пропозиції
@bot.message_handler(func=lambda message: message.text == bt.suport_offer)
def write_offer(message):
    msg = bot.send_message(message.chat.id, 'Напишіть у повідомленні',
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, offer)


# Записує відгук у файл offer.txt
def offer(message):
    text_write.write_offer(message)
    bot.send_message(message.chat.id, 'Дякуєм за відгук', reply_markup=support)


@bot.message_handler(func=lambda message: message.text == bt.support_donate)
def donate(message):
    bot.send_message(message.chat.id, '''
BTC - 1J18ggoGFnbhAGg66aGScXTEJbk7S5Xu6S
ETH - 0x3AA1a0dAfC77Ea0fb28b84F1065565Ac25e82a94
Monon - 5375411405204616
Privat24 - 4149497110373257''', reply_markup=support)


@bot.message_handler(func=lambda message: message.text == bt.suport_back)
def back(message):
    bot.send_message(message.chat.id, 'Головне меню', reply_markup=main)


@bot.message_handler(func=lambda message: message.text == bt.portfolio)
def portfolio(message):
    bot.send_message(message.chat.id, 'Створи криптопортфель з улюбленими монетами',
                     reply_markup=portfolio_menu)


@bot.message_handler(func=lambda message: message.text == bt.add_marker)
def add_marker(message):
    database.create_table(message)
    msg = bot.send_message(message.chat.id, 'Вкажи маркер монети наприклад BTC',
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, add_id)


def add_id(message):
    try:
        database.insert_to_table(coingecko.chcek_marker(message.text), message)
        bot.send_message(message.chat.id, 'Маркер додано',
                         reply_markup=portfolio_menu)
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, 'Цей маркер уже в портфелі',
                         reply_markup=portfolio_menu)
    except IndexError:
        bot.send_message(message.chat.id, 'Такого маркера не існує',
                         reply_markup=portfolio_menu)


@bot.message_handler(func=lambda message: message.text == bt.portfolio_status)
def portfolio_status(message):
    try:
        coin_keyboard = database.status_keyboard(message)
        bot.send_message(message.chat.id, database.select_id(message),
                         reply_markup=coin_keyboard)
    except Exception:
        bot.send_message(message.chat.id, 'Твій портфель порожній')


@bot.message_handler(func=lambda message: message.text == bt.add_value)
def add_value(message):
    try:
        bot.send_message(message.chat.id, 'Обери монету',
                         reply_markup=database.add_value(message))
    except Exception:
        bot.send_message(message.chat.id, 'Твій портфель порожній')


@bot.message_handler(func=lambda message: message.text == bt.delete_marker)
def del_coin(message):
    try:
        bot.send_message(message.chat.id, 'Обери монету яку потрібно видалити',
                         reply_markup=database.delete_coin(message))
    except Exception:
        bot.send_message(message.chat.id, 'Твій портфель порожній')


@bot.message_handler(func=lambda message: message.text == bt.delete_portfolio)
def delete_portfolio(message):
    try:
        database.drop_table(message)
        bot.send_message(message.chat.id, 'Твій портфель видалено')
    except Exception:
        bot.send_message(message.chat.id, 'Ой шось пішло не так')


@bot.message_handler(func=lambda message: message.text == bt.add_price)
def add_price(message):
    try:
        bot.send_message(message.chat.id, 'Обери монету до якої потрібно додати ціну покупки',
                         reply_markup=database.add_value_price(message))
    except Exception:
        bot.send_message(message.chat.id, 'Твій портфель порожній')


@bot.message_handler(func=lambda message: message.text == bt.add_transaction)
def add_transaction(message):
    try:
        bot.send_message(message.chat.id, 'Обери монету',
                         reply_markup=database.add_transact(message))
    except Exception:
        bot.send_message(message.chat.id, 'Твій портфель порожній')


@bot.callback_query_handler(func=lambda call: call.data in database.select_value_coin(call))
def inline_add_value(call):
    msg = bot.send_message(call.message.chat.id, f'Введи кількість монет {call.data.capitalize()}',
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, insert_value, call.data)


@bot.callback_query_handler(func=lambda call: call.data in database.delete_coin_id(call.message))
def inline_del_coin(call):
    database.del_coin(call.data, call.message)
    bot.send_message(call.message.chat.id, f'{call.data.capitalize()[0:-4]} видалено')


@bot.callback_query_handler(func=lambda call: call.data in database.select_id(call.message)[1])
def inline_portfolio(call):
    all_cost = database.select_id(call.message)[0]
    coin_dict = database.select_id(call.message)[1].get(call.data)
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'{coin_dict} {all_cost}',
                              reply_markup=database.status_keyboard(call.message))
    except telebot.apihelper.ApiTelegramException:
        pass


@bot.callback_query_handler(func=lambda call: call.data in database.select_price_coin(call))
def inline_add_price(call):
    msg = bot.send_message(call.message.chat.id, f'Введи ціну покупки {call.data.capitalize()[0:-6]} в USD',
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, insert_price)


@bot.callback_query_handler(func=lambda call: call.data in database.select_transact(call))
def inline_add_trans(call):
    msg = bot.send_message(call.message.chat.id, f'Введи кількість монет {call.data.capitalize()[0:-6]}',
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_value, call.data)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
def back_to_menu(call):
    msg = bot.send_message(call.message.chat.id, "Головне меню", reply_markup=main)
    bot.clear_step_handler(msg)


def insert_value(data, message):
    try:
        database.add_value_coin(data, message)
        bot.send_message(data.from_user.id, f'{message.capitalize()} додано',
                         reply_markup=portfolio_menu)
    except sqlite3.OperationalError:
        bot.send_message(data.from_user.id, 'Щось пішло не так',
                         reply_markup=portfolio_menu)


def insert_price(data, message):
    try:
        database.add_price(data, message)
        bot.send_message(data.from_user.id, f'Ціна покупки {message.capitalize()[0:-6]} додано',
                         reply_markup=portfolio_menu)
    except sqlite3.OperationalError:
        bot.send_message(data.from_user.id, 'Щось пішло не так',
                         reply_markup=portfolio_menu)


@bot.message_handler(func=lambda message: message.text == bt.history_coin)
def history_price(message):
    msg = bot.send_message(message.chat.id, 'Вкажи маркер монети наприклад BTC',
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_symbol)


def get_symbol(message):
    try:
        symbol = coingecko.check_id(message.text.lower())
        msg = bot.send_message(message.chat.id, 'Вкажи дату у форматі дд-мм-рр\nНаприклад 02-02-2021',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_history_price, symbol)
    except Exception:
        msg = bot.send_message(message.chat.id, 'Монету не знайдено\nСпробуй ще раз ',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_symbol)


def get_history_price(message, symbol):
    try:
        bot.send_message(message.chat.id, coingecko.history_coin(message.text, symbol), reply_markup=main)
    except Exception:
        bot.send_message(message.chat.id, 'Щось пішло не так', reply_markup=main)


def save_value(message, coin_id):
    try:
        coin_value = float(message.text.replace(",", "."))
        coin_id = coin_id[0:-6]
        msg = bot.send_message(message.from_user.id, f'Вкажи ціну покупки')
        bot.register_next_step_handler(msg, save_price, coin_value, coin_id)
    except ValueError:
        bot.send_message(message.chat.id, 'Вводь цифри', reply_markup=portfolio_menu)


def save_price(message, coin_value, coin_id):
    try:
        table_name = f'{message.from_user.first_name}_{message.from_user.id}'
        coin_data = list()
        coin_data.append(table_name)
        coin_data.append(coin_id)
        coin_data.append(coin_value)
        coin_data.append(float(message.text.replace(",", ".")))
        bot.send_message(message.from_user.id,
                         f'Середня ціна покупки\n{coin_id.capitalize()} {database.transaction(coin_data)} USD',
                         reply_markup=portfolio_menu)
    except ValueError:
        bot.send_message(message.chat.id, 'Вводь цифри', reply_markup=portfolio_menu)


@bot.message_handler(func=lambda message: message.text == bt.erc20)
def erc_20(message):
    msg = bot.send_message(message.from_user.id, 'Вкажи Ethereum адресу')
    bot.register_next_step_handler(msg, balance_erc20)


def balance_erc20(message):
    try:
        bot.send_message(message.from_user.id, etherscan.balance_erc20(message.text))
        result = etherscan.get_erc721(message.text)
        dict_nft = result[1]
        print(dict_nft)
        if len(dict_nft) > 0:
            bot.send_message(message.from_user.id, '⬇️ NFT', reply_markup=result[0])
        else:
            pass

        @bot.callback_query_handler(func=lambda call: call.data in result[1])
        def edit_image(call):
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=dict_nft[call.data],
                                      reply_markup=result[0])
            except telebot.apihelper.ApiTelegramException:
                pass
    except Exception:
        bot.send_message(message.from_user.id, 'Ethereum адреса невірна')


bot.infinity_polling()
