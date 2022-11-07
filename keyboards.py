import pprint

import telebot
from buttons import Buttons

bt = Buttons()
main = telebot.types.ReplyKeyboardMarkup(True)
main.row(bt.info, bt.history_coin)
main.row(bt.portfolio_status, bt.portfolio)
main.row(bt.support, bt.erc20)

support = telebot.types.ReplyKeyboardMarkup(True)
support.row(bt.suport_offer, bt.support_donate)
support.row(bt.suport_back)

portfolio_menu = telebot.types.ReplyKeyboardMarkup(True)
portfolio_menu.row(bt.add_marker, bt.add_transaction)
portfolio_menu.row(bt.delete_portfolio, bt.delete_marker)
portfolio_menu.row(bt.suport_back)

back_to_menu = telebot.types.InlineKeyboardMarkup()
item_back = telebot.types.InlineKeyboardButton(text='Відміна', callback_data='back_to_menu')
back_to_menu.add(item_back)


def inline_keyboards(coin_list):
    add_value = telebot.types.InlineKeyboardMarkup()
    coin_data = [coins for coins in coin_list[::2]]
    coin_text = [names for names in coin_list[1::2]]
    button_list = [telebot.types.InlineKeyboardButton(text=cointext, callback_data=coindata) for cointext, coindata
                   in zip(coin_text, coin_data)]
    add_value.add(*button_list)
    return add_value


def inline_keyboard_del(coin_list):
    delete_coin = telebot.types.InlineKeyboardMarkup()
    coin_data = [coins + '_del' for coins in coin_list[::2]]
    coin_text = [names for names in coin_list[1::2]]
    button_list = [telebot.types.InlineKeyboardButton(text=cointext, callback_data=coindata)
                   for cointext, coindata in zip(coin_text, coin_data)]

    delete_coin.add(*button_list)
    return delete_coin


def inline_keyboard_stat(coin_list):
    stat_portfolio = telebot.types.InlineKeyboardMarkup()
    coin_data = [coins + '_key' for coins in coin_list[::2]]
    coin_text = [names for names in coin_list[1::2]]
    if len(coin_data) > 1:
        button_list = [telebot.types.InlineKeyboardButton(text=cointext, callback_data=coindata)
                       for cointext, coindata in zip(coin_text, coin_data)]

        stat_portfolio.add(*button_list)
        return stat_portfolio
    else:
        return None


def inline_add_price(coin_list):
    add_price = telebot.types.InlineKeyboardMarkup()
    coin_data = [coins + '_price' for coins in coin_list[::2]]
    coin_text = [names for names in coin_list[1::2]]
    button_list = [telebot.types.InlineKeyboardButton(text=cointext, callback_data=coindata) for cointext, coindata
                   in zip(coin_text, coin_data)]
    add_price.add(*button_list)
    return add_price


def inline_add_transaction(coin_list):
    add_price = telebot.types.InlineKeyboardMarkup()
    coin_data = [coins + '_tarns' for coins in coin_list[::2]]
    coin_text = [names for names in coin_list[1::2]]
    button_list = [telebot.types.InlineKeyboardButton(text=cointext, callback_data=coindata) for cointext, coindata
                   in zip(coin_text, coin_data)]
    add_price.add(*button_list)
    return add_price


def inline_erc721(nft_dict):
    nft = telebot.types.InlineKeyboardMarkup()
    coin_data = [coins for coins in nft_dict]
    button_list = [telebot.types.InlineKeyboardButton(text=coindata, callback_data=coindata) for coindata in coin_data]
    nft.add(*button_list)
    return nft, nft_dict
