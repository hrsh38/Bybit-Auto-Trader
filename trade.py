from bybit_api import *
from test import *
import math

text = """
🪙 Coin: PENDLE
📈 Direction: Short Limit
⚔️  Leverage 3x to 25x
💎 Entry Zone: 6.0400 to 6.8500
🔴 Stop Loss: 7.1000 BE and Risk level - Medium

🟢 TP1: 5.8600 done
🟢 TP2: 5.5300 done
🟢 TP3: 4.7500
🟢 TP4: 3.9600
🟢 TP5: 2.4100
🟢 TP6: 1

<@&1211361822167277619>
"""
# {'Coin': 'PENDLE', 'Direction': 'Short Limit', 'Entry Zone': (6.04, 6.85),
#   'Stop Loss': 7.1, 'Risk Level': 'Medium', 'TP': {'1': 5.86, '2': 5.53, '3': 4.75, '4': 3.96, '5': 2.41, '6': 1.0}}

side_dict = {
    "Short": "Sell",
    "Long": "Buy"
}


def execute_trade(trade):
    print(trade)
    quantity = math.ceil(10000/trade['Entry Zone'][0])
    side = trade['Direction'].split(' ')
    positions = get_all_positions()
    print(positions)
    print(quantity)
    if(len(side)==1):
        # MARKET ORDER
        res = set_market_order(trade['Coin']+'USDT', quantity, side_dict[side[0]], trade['Stop Loss'])
        print(res)
    for entry_prices in trade['Entry Zone']:
        res = set_limit_order(trade['Coin']+'USDT', quantity, entry_prices, side_dict[side[0]], trade['Stop Loss'])
        print(res)



trade = extract_info(text)
execute_trade(trade)


