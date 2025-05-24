from bybit_api import *
from pybit.unified_trading import WebSocket
from test import *
import math
from time import sleep

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
# print(extract_info(text))
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
        res = set_market_order(trade['Coin'], quantity, side_dict[side[0]], trade['Stop Loss'])
        print(res)
    for entry_prices in trade['Entry Zone']:
        res = set_limit_order(trade['Coin'], quantity, entry_prices, side_dict[side[0]], trade['Stop Loss'])
        print(res)


def within_percent(arr, num):
    print(arr, num)
    for i, val in enumerate(arr):
        if 0.99*num<= val <= 1.01*num:
            return i
    return None  # Return None if no value is within the range

print(within_percent([0.002029, 0.002176, 0.002279, 0.002425, 0.00255, 0.0035], 0.002028))
# def check_and_delete():
#     positions = get_all_positions()
#     symbols = [d['symbol'] for d in positions]
#     # print(symbols)
#     query = {'Coin': {'$nin': symbols}}  # Select coins that are NOT in the positions list
#     result = collection.delete_many(query)
#     print(f"Deleted {result.deleted_count} inactive coin signals.")


# print(get_positions('DOGEUSDT'))
# [{'symbol': 'DOGEUSDT', 'leverage': '75', 'autoAddMargin': 0, 'avgPrice': '0.13297595', 'liqPrice': '', 
#   'riskLimitValue': '200000', 'takeProfit': '', 'positionValue': '20042.93333707', 'isReduceOnly': False, 
#   'tpslMode': 'Full', 'riskId': 206, 'trailingStop': '0', 'unrealisedPnl': '146.81436293', 'markPrice': '0.13395',
#     'adlRankIndicator': 2, 'cumRealisedPnl': '-12.89327281', 'positionMM': '161.19869867', 'createdTime': '1714686266151',
#       'positionIdx': 0, 'positionIM': '278.11594342', 'seq': 116123678933, 'updatedTime': '1714705149462', 'side': 'Buy',
#         'bustPrice': '', 'positionBalance': '0', 'leverageSysUpdatedTime': '', 'curRealisedPnl': '-12.89327281', 'size': '150726',
#    'positionStatus': 'Normal', 'mmrSysUpdatedTime': '', 'stopLoss': '0.1178', 'tradeMode': 0, 'sessionAvgPrice': ''}]
# add_sl('DOGEUSDT', 0.1178)
# symbol = 'DOGEUSDT'
# pos = get_positions(symbol)[0]
# num_of_tps = 5
# size = float(pos['size'])/num_of_tps
# set_tp(symbol,size, 0.14083)
# trade = extract_info(text)
# execute_trade(trade)
# delete_dca_orders('DOGEUSDT')
# add_sl('DOGEUSDT', 0.1179)

# pybit WebSocket Setup
# ws = WebSocket(
#     testnet=False,
#     channel_type="private",
#     api_key = "3R7xbpnTG4apkrPHhE",
#     api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"
# )


# # Logic for stream
# def handle_stream(message):

#     print(message)

# ws.execution_stream(callback=handle_stream)


# while True:
#     sleep(1)