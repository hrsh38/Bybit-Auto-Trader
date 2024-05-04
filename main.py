import discord
import pymongo
from pymongo import MongoClient
from test import *
from bybit_api import *
from pybit.unified_trading import WebSocket
from trade import execute_trade
# from your_extraction_module import extract_info  # Make sure to replace this with the actual path to your extraction logic

# MongoDB connection setup
client_mongo = MongoClient('mongodb://localhost:27017/')  # Update the connection string as necessary
db = client_mongo['trading_signals']  # Name of the database
collection = db['signals']  # Name of the collection

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Extract trading information from the message
    trade_info = extract_info(message.content)
    check_and_delete()
    if trade_info:
        query = {'Coin': trade_info['Coin']}
        existing_trade = collection.find_one(query)
        # Update database and decide if trading should proceed
        set_max_lev(trade_info['Coin'])
        update_or_create_trade_signal(trade_info)
        if existing_trade:
            print('add in TPs')
            symbol = trade_info['Coin']
            num_of_tps = len(trade_info['TP'])
            delete_tp_orders(symbol)
            pos = get_positions(symbol)[0]
            if(num_of_tps > 0):
                size = float(pos['size'])/num_of_tps
                for i in range(num_of_tps):
                    set_tp(symbol, size, trade_info['TP'][i])
        else:
            execute_trades(trade_info)

def check_and_delete():
    positions = get_all_positions()
    symbols = [d['symbol'] for d in positions]
    # print(symbols)
    query = {'Coin': {'$nin': symbols}}  # Select coins that are NOT in the positions list
    result = collection.delete_many(query)
    print(f"Deleted {result.deleted_count} inactive coin signals.")

def update_or_create_trade_signal(trade_info):
    """ Updates an existing trade signal or creates a new one if it doesn't exist. """
    query = {'Coin': trade_info['Coin']}
    update = {"$set": trade_info}
    options = True
    collection.update_one(query, update, options)
    print(f"Signal processed for {trade_info['Coin']} - updated or inserted as needed.")

def execute_trades(trade_info):
    """ Logic to execute trade based on updated trade_info """
    print(f"Executing trade for {trade_info['Coin']}")
    execute_trade(trade_info)
    
    # Add your trading logic here, which may involve calling a trading API or executing other actions
def closest_index(arr, num):
    closest_idx = min(range(len(arr)), key=lambda i: abs(arr[i] - num))
    return closest_idx

def within_percent(arr, num):
    print(arr, num)
    threshold = 0.01 * num  # 1% of the input number
    for i, val in enumerate(arr):
        if (1 - threshold) * num <= val <= (1 + threshold) * num:
            return i
    return None  # Return None if no value is within the range


# pybit WebSocket Setup
ws = WebSocket(
    testnet=False,
    channel_type="private",
    api_key = "3R7xbpnTG4apkrPHhE",
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"
)
# h = {'topic': 'execution', 'id': '130425540_DOGEUSDT_116080561182', 'creationTime': 1714694000130,
#       'data': [{'category': 'linear', 'symbol': 'DOGEUSDT', 'closedSize': '50', 'execFee': '0.00363275',
#                  'execId': 'f4f44265-636a-54c0-8a85-d4d10a3d2485', 'execPrice': '0.1321', 'execQty': '50', 
#                  'execType': 'Trade', 'execValue': '6.605', 'feeRate': '0.00055', 'tradeIv': '', 'markIv': '', 
#                  'blockTradeId': '', 'markPrice': '0.13209', 'indexPrice': '', 'underlyingPrice': '', 'leavesQty': '0',
#                    'orderId': 'f356aa12-14d2-4730-b44a-245f9c8a557b', 'orderLinkId': '', 'orderPrice': '0.12549',
#                      'orderQty': '50', 'orderType': 'Market', 'stopOrderType': 'PartialTakeProfit', 'side': 'Sell',
#                        'execTime': '1714694000128', 'isLeverage': '0', 'isMaker': False, 'seq': 116080561182, 'marketUnit': '', 
#                        'createType': 'CreateByPartialTakeProfit'}]}


# Logic for stream
def handle_stream(message):
    # print(message)
    try:
        orderType=message['data'][0]['orderType']#market = TP, #limit = DCA
        stopOrderType = message['data'][0]['stopOrderType']
        symbol= message['data'][0]['symbol']
        tp_price = message['data'][0]['execPrice']
        query = {'Coin': symbol}
        coin = collection.find_one(query)
        # print(coin)
        print(tp_price, orderType, stopOrderType)
        pos = get_positions(symbol)[0]
        #Case 1
        
        #DCA gets filled -> update the TP's
        if(orderType == 'Limit'):
            print('add in TPs')
            symbol = coin['Coin']
            num_of_tps = len(coin['TP'])
            delete_tp_orders(symbol)
            if(num_of_tps > 0):
                size = float(pos['size'])/num_of_tps
                for i in range(num_of_tps):
                    set_tp(symbol, size, coin['TP'][i])
        #Case 2
        #TP's hit -> cancel all other DCA orders and move stop loss up accordingly
        if(orderType == 'Market' and stopOrderType == 'PartialTakeProfit'):
            delete_dca_orders(symbol)
            index = within_percent(coin['TP'], float(tp_price))
            print(index)
            if(index == 0):
                add_sl(symbol, float(pos['avgPrice']))
            elif(index > 0):
                add_sl(symbol, coin['TP'][index - 1])
            else:
                print('Not within range')
        check_and_delete()
        #figure out which TP it is
    except:
        print('ERROR')
        # print(message)

check_and_delete()
ws.execution_stream(callback=handle_stream)
print('ws is ready')
# Enter your bot's token here
BOT_TOKEN = 'MTE5NDUxMjc1ODU5OTg1MjA1Mg.GJYbaG._jSuN1noAtO2JOo9ZW8PrEYZBEbadUJImkcrpw'
client.run(BOT_TOKEN)

