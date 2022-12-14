from etherscan_shady import etherscan

import keyboards
from config import APY_KEY
from config import provider_url


def balance_erc20(address):
    text = ''
    balance = etherscan.GetResult(address, APY_KEY)
    result_erc20 = balance.get_erc20_balance()
    result_eth = round(balance.get_eth_balance(), 5)
    text += f'ā ETH - {result_eth}\nā¬ ERC20\n'
    dict_items = result_erc20.items()
    if len(dict_items) == 0:
        return f'ā ETH - {result_eth}'
    for i in dict_items:
        symbol = i[0]
        value = round(i[1], 5)
        text += f'ā {symbol} - '
        text += f'{value}\n'
    return text


def get_erc721(address):
    balance = etherscan.GetResult(address, APY_KEY)
    erc721 = balance.get_erc721_balance(provider_url)
    return keyboards.inline_erc721(erc721)
