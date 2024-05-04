
from logging import error
from pybit.unified_trading import HTTP


def get_positions(symbol):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )

    coins = []
    # Fetch positions
    positions_response = session.get_positions(category="linear", settleCoin="USDT", symbol=symbol)
    positions = positions_response.get('result', {}).get('list', [])
    # print(positions)
    return positions

def get_all_positions():
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )

    coins = []
    # Fetch positions
    positions_response = session.get_positions(category="linear", settleCoin="USDT")
    positions = positions_response.get('result', {}).get('list', [])
    # print(positions)
    return positions


def add_sl(symbol, stopLoss):
    print("ADDING SL")
    # print(symbol, stopLoss)
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    res = session.set_trading_stop(category='linear', orderType="Market",symbol=symbol,tpslMode="Full", stopLoss=stopLoss, slOrderType="Market")
    print(res)

def close_market(symbol, qty, side):
     # print(symbol, stopLoss)
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    session.place_order(category='linear',symbol=symbol, side=side, order_type="Market", qty= qty)
    

# add_sl('ETHUSDT', )

def set_market_order(symbol, quantity, side, stop_loss):
    try:
        api_key = "3R7xbpnTG4apkrPHhE"
        api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

        session = HTTP(
            api_key=api_key,
            api_secret=api_secret
        )
        res = session.place_order( category='linear', orderType="Market",symbol=symbol, side=side, qty=quantity, stopLoss = stop_loss)
        print(res)
    except:
        print(error)

def set_limit_order(symbol, quantity, limit_price, side, stop_loss):
    try:
        api_key = "3R7xbpnTG4apkrPHhE"
        api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

        session = HTTP(
            api_key=api_key,
            api_secret=api_secret
        )
        res = session.place_order( category='linear', orderType="Limit",symbol=symbol, side=side, qty=quantity, price = limit_price , stopLoss = stop_loss)
        print(res)
    except:
        print(error)

def set_trailing_sl(symbol, trailingStop):
    try:
        api_key = "3R7xbpnTG4apkrPHhE"
        api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

        session = HTTP(
            api_key=api_key,
            api_secret=api_secret
        )
        res = session.set_trading_stop(category='linear', orderType="Market",symbol=symbol,tpslMode="Full", trailingStop=trailingStop, slOrderType="Market")
        print(res)
    except:
        print(error)
    # return(res['retMsg'])
# set_dca('TIAUSDT', 15, "4.0", 13, "Buy")
# fetch_and_normalize_data()
# set_market_order('ETHUSDT',1, "Sell")
# positions = get_positions('ETHUSDT')[0]
# if(positions.get('side') == 'Sell'):
#     add_sl('ETHUSDT', float(positions.get('avgPrice'))+4)
# else:
#     add_sl('ETHUSDT', float(positions.get('avgPrice'))-4)

# # add_sl(positions)
# print(float(positions.get('avgPrice'))+1)




def get_account_value():
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )

    account_response = session.get_wallet_balance(accountType="UNIFIED")
    account = account_response.get('result', {}).get('list', [])[0]
    return account
    #  return positions_response['totalWalletBalance']


def combine_entries(entries):
    combined_entries = []
    current_combined = None

    for entry in entries:
        if current_combined is None:
            # Start a new combination
            current_combined = entry
            current_combined['type'] = 'not'
        elif current_combined['createdTime'] == entry['createdTime']:
            current_combined['type'] = 'tpsl'
            # Combine current entry with the existing combination
            for key in entry:
                if key in current_combined:
                    if current_combined[key] == entry[key]:
                        # Same value, no action needed
                        continue
                    elif isinstance(current_combined[key], list):
                        # Already a list, add new value if it's not already in the list
                        if entry[key] not in current_combined[key]:
                            current_combined[key].append(entry[key])
                    else:
                        # Different value, create a list
                        current_combined[key] = [current_combined[key], entry[key]]
        else:
            # Different createdTime, add the previous combination to the list and start a new one
            combined_entries.append(current_combined)
            current_combined = entry

    # Add the last combined entry if it exists
    if current_combined is not None:
        combined_entries.append(current_combined)

    return combined_entries


# fetch_and_normalize_data()

# Parameters for the TPSL

def set_tp(symbol,quantity, takeProfit):
    print("SETTING TPSL")
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    

    # print(symbol, quantity, takeProfit, stopLoss)
    # takeProfit can be string or float, quanity has to be a string
    res = session.set_trading_stop(category='linear', orderType="Market",symbol=symbol,tpslMode="Partial", takeProfit= float(takeProfit), tpSize= str(quantity))
    print(res)
    return res


# set_tpsl("TIAUSDT", "1000", 14.0, 13.5)



def get_prices():
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )

    # Fetch positions
    positions_response = session.get_positions(category="linear", settleCoin="USDT")
    positions = positions_response.get('result', {}).get('list', [])
    prices = {}
    # Fetch open orders
    for position in positions:
        symbol = position.get('symbol')
        price_response = session.get_tickers(category="linear", symbol=symbol)
        price = price_response.get('result', {}).get('list', [])[0]
        # print(price)
        prices[symbol] = price['lastPrice']
    # print(prices)
    return prices
# get_prices()
def delete_tp_orders(symbol):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    try:
        open_orders = session.get_open_orders(category = 'linear', symbol = symbol).get('result', {}).get('list', [])
        for order in open_orders:
            if(order['stopOrderType'] == 'PartialTakeProfit'):
                delete_order(symbol, order['orderId'])
    except:
        print('No orders')

def delete_dca_orders(symbol):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    try:
        open_orders = session.get_open_orders(category = 'linear', symbol = symbol).get('result', {}).get('list', [])
        for order in open_orders:
            if(order['orderType'] == 'Limit'):
                delete_order(symbol, order['orderId'])
    except:
        print('No orders')

def delete_all_orders(symbol):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    try:
        open_orders = session.get_open_orders(category = 'linear', symbol = symbol).get('result', {}).get('list', [])[0]['orderId']
        delete_order(symbol, open_orders)
        print(open_orders)
    except:
        print('No orders')

def delete_order(symbol, orderId):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    res = session.cancel_order(category="linear", symbol = symbol, orderId=orderId)
    print(res)
    return(res['retMsg'])

def test_func(symbol):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )


def set_max_lev(symbol):
    api_key = "3R7xbpnTG4apkrPHhE"
    api_secret = "RHy4YMHIGyL2jla4WwWT2AwnjBpxUclbegRR"

    session = HTTP(
        api_key=api_key,
        api_secret=api_secret
    )
    res = session.get_risk_limit(category="linear",symbol=symbol).get('result', {}).get('list', [])
    maxLev = res[0]['maxLeverage']
    res = session.set_leverage(category="linear",symbol=symbol,buyLeverage=maxLev,sellLeverage=maxLev)
    print(res)
