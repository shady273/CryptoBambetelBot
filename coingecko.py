import pprint

from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_token_price(symbol):
    check_symbol = cg.get_coins_list()
    filtered = filter(lambda x: x['symbol'] == symbol.lower(), check_symbol)
    statuses = [x['id'] for x in filtered]
    statuses.sort(key=len)
    coin_data = cg.get_coin_by_id(id=statuses[0])
    name = coin_data['name']
    try:
        price = "{:,.3f}".format(coin_data['market_data']['current_price']['usd'])
    except Exception:
        price = 0
    try:
        market_cap = "{:,.2f}".format(coin_data['market_data']['market_cap']['usd'])
    except Exception:
        market_cap = 0
    try:
        price_change_24h = "{:,.2f}".format(coin_data['market_data']['price_change_percentage_24h'])
    except Exception:
        price_change_24h = 0

    text = f'''
✅ {name}
❇ Ціна {price} - USD
📈 Зміна ціни 24h  {price_change_24h} %
💰 Капіталізація {market_cap} - USD
'''

    return text


def chcek_marker(marker):
    check_symbol = cg.get_coins_list()
    filtered = filter(lambda x: x['symbol'] == marker.lower(), check_symbol)
    statuses = [x['id'] for x in filtered]
    statuses.sort(key=len)
    coin_data = cg.get_coin_by_id(id=statuses[0])
    name = coin_data['name']
    result = list()
    result.append(statuses[0])
    result.append(name)

    return result


def portfolio(coin_list):
    all_smile = str
    text = ''
    all_cost = list()
    all_profit = list()
    coin_id = [coins for coins in coin_list[::4]]
    portfolio_status = cg.get_price(ids=coin_id, vs_currencies='usd', include_24hr_change=True)
    coin_name = [names for names in coin_list[1::4]]
    coin_value = [value for value in coin_list[2::4]]
    coin_by_price = [value for value in coin_list[3::4]]
    thisdict = dict()
    for coin, names, values, by_price in zip(coin_id, coin_name, coin_value, coin_by_price):
        name = names
        value = values
        coin_key = coin + '_key'
        price = portfolio_status[coin]['usd']
        change = portfolio_status[coin]['usd_24h_change']
        if change is None:
            change = 0
        cost = value * price
        by_cost = round(value * by_price)
        profit = cost - by_cost
        if profit < 0:
            smile = '🔴 Втрати'
        else:
            smile = '🟢 Профіт'
        all_cost.append(cost)
        all_profit.append(profit)

        string = f'''✅ {name}
❇ Ціна {price} - USD
📈 Зміна за 24 год {"{:.1f}".format(change)} %
🪙 Кількість {round(value, 1) if value > 1 else round(value, 5)}
💵 Вартість {round(cost, 1) if cost > 1 else round(cost, 5)} - USD
💲 Ціна покупки {round(by_price, 1) if by_price > 1 else round(by_price, 5)} - USD
{smile} {round(profit, 1) if profit > 1 or profit < 0 else round(profit, 5)} - USD
'''
        thisdict[coin_key] = string
        text += string
        if sum(all_profit) < 0:
            all_smile = '🔴 Втрати'
        else:
            all_smile = '🟢 Профіт'
    sum_portfel = f'''
💼 Вартість портфеля {round(sum(all_cost), 1) if sum(all_cost) > 1 else round(sum(all_cost), 5)} - USD
{all_smile} {round(sum(all_profit), 1) if sum(all_profit) > 1 or sum(all_profit) < 0 
    else round(sum(all_profit), 5)} - USD'''
    text += sum_portfel
    list_portfolio = list()
    list_portfolio.append(sum_portfel)
    list_portfolio.append(thisdict)
    if len(coin_id) > 1:
        return list_portfolio
    else:
        return text


def history_coin(date, symbol):
    histori_coin = cg.get_coin_history_by_id(id=symbol.lower(), date=date)
    coin_price = histori_coin['market_data']['current_price']['usd']
    if coin_price > 1:
        coin_price = float(coin_price)
        coin_price = "{:,.1f}".format(coin_price)
    else:
        coin_price = "{:,.5f}".format(coin_price)
    coin_name = histori_coin['name']
    text = f'''❇ {coin_name} - {coin_price} USD'''
    return text


def check_id(symbol):
    check_symbol = cg.get_coins_list()
    filtered = filter(lambda x: x['symbol'] == symbol.lower(), check_symbol)
    statuses = [x['id'] for x in filtered]
    statuses.sort(key=len)
    return statuses[0]
