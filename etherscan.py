from etherscan_shady import etherscan
from config import APY_KEY


def balance_erc20(address):
    text = ''
    balance = etherscan.GetResult(address, APY_KEY)
    result_erc20 = balance.get_erc20_balance()
    result_eth = round(balance.get_eth_balance(), 5)
    text += f'❇ ETH - {result_eth}\n⬇ ERC20\n'
    dict_items = result_erc20.items()
    if len(dict_items) == 0:
        return f'✅ ETH - {result_eth}'
    for i in dict_items:
        symbol = i[0]
        value = round(i[1], 5)
        text += f'✅ {symbol} - '
        text += f'{value}\n'
    return text

