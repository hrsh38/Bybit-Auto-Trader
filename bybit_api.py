from logging import error
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_bybit_session():
    """
    Create and return a Bybit session with API credentials from environment variables.
    
    Returns:
        HTTP: A configured Bybit HTTP client session
        
    Raises:
        ValueError: If API credentials are not found in environment variables
    """
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    
    if not api_key or not api_secret:
        raise ValueError("Bybit API credentials not found in environment variables")
    
    return HTTP(
        api_key=api_key,
        api_secret=api_secret
    )

def get_positions(symbol):
    """
    Get positions for a specific trading symbol.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        list: List of position information for the specified symbol
    """
    session = get_bybit_session()
    positions_response = session.get_positions(category="linear", settleCoin="USDT", symbol=symbol)
    positions = positions_response.get('result', {}).get('list', [])
    return positions

def get_all_positions():
    """
    Get all open positions across all trading pairs.
    
    Returns:
        list: List of all open positions in the account
    """
    session = get_bybit_session()
    positions_response = session.get_positions(category="linear", settleCoin="USDT")
    positions = positions_response.get('result', {}).get('list', [])
    return positions

def add_sl(symbol, stopLoss):
    """
    Add a stop loss order to an existing position.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        stopLoss (float): The stop loss price level
        
    Note:
        This function will place a market stop loss order that will trigger
        when the price reaches the specified stop loss level.
    """
    print("ADDING SL")
    session = get_bybit_session()
    res = session.set_trading_stop(
        category='linear',
        orderType="Market",
        symbol=symbol,
        tpslMode="Full",
        stopLoss=stopLoss,
        slOrderType="Market"
    )
    print(res)

def close_market(symbol, qty, side):
    """
    Close a position with a market order.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        qty (float): The quantity to close
        side (str): The side of the order ('Buy' or 'Sell')
        
    Note:
        Use 'Buy' to close a short position and 'Sell' to close a long position.
    """
    session = get_bybit_session()
    session.place_order(
        category='linear',
        symbol=symbol,
        side=side,
        order_type="Market",
        qty=qty
    )

def set_market_order(symbol, quantity, side, stop_loss):
    """
    Place a market order with an attached stop loss.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        quantity (float): The order quantity
        side (str): The side of the order ('Buy' or 'Sell')
        stop_loss (float): The stop loss price level
        
    Note:
        The stop loss will be placed immediately after the market order is filled.
    """
    try:
        session = get_bybit_session()
        res = session.place_order(
            category='linear',
            orderType="Market",
            symbol=symbol,
            side=side,
            qty=quantity,
            stopLoss=stop_loss
        )
        print(res)
    except Exception as e:
        print(f"Error placing market order: {e}")

def set_limit_order(symbol, quantity, limit_price, side, stop_loss):
    """
    Place a limit order with an attached stop loss.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        quantity (float): The order quantity
        limit_price (float): The limit price for the order
        side (str): The side of the order ('Buy' or 'Sell')
        stop_loss (float): The stop loss price level
        
    Note:
        The stop loss will be placed only if the limit order is filled.
    """
    try:
        session = get_bybit_session()
        res = session.place_order(
            category='linear',
            orderType="Limit",
            symbol=symbol,
            side=side,
            qty=quantity,
            price=limit_price,
            stopLoss=stop_loss
        )
        print(res)
    except Exception as e:
        print(f"Error placing limit order: {e}")

def set_trailing_sl(symbol, trailingStop):
    """
    Set a trailing stop loss for an existing position.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        trailingStop (float): The trailing stop distance in price units
        
    Note:
        A trailing stop loss will follow the price movement and only trigger
        when the price moves against the position by the specified distance.
    """
    try:
        session = get_bybit_session()
        res = session.set_trading_stop(
            category='linear',
            orderType="Market",
            symbol=symbol,
            tpslMode="Full",
            trailingStop=trailingStop,
            slOrderType="Market"
        )
        print(res)
    except Exception as e:
        print(f"Error setting trailing stop: {e}")

def get_account_value():
    """
    Get the current account wallet balance and equity.
    
    Returns:
        dict: Account information including wallet balance, equity, and other metrics
    """
    session = get_bybit_session()
    account_response = session.get_wallet_balance(accountType="UNIFIED")
    account = account_response.get('result', {}).get('list', [])[0]
    return account

def combine_entries(entries):
    """
    Combine multiple trading entries into a single entry for analysis.
    
    Args:
        entries (list): List of trading entries to combine
        
    Returns:
        list: Combined entries with merged information
        
    Note:
        This function is useful for analyzing related orders (e.g., entry and stop loss)
        that were placed at the same time.
    """
    combined_entries = []
    current_combined = None

    for entry in entries:
        if current_combined is None:
            current_combined = entry
            current_combined['type'] = 'not'
        elif current_combined['createdTime'] == entry['createdTime']:
            current_combined['type'] = 'tpsl'
            for key in entry:
                if key in current_combined:
                    if current_combined[key] == entry[key]:
                        continue
                    elif isinstance(current_combined[key], list):
                        if entry[key] not in current_combined[key]:
                            current_combined[key].append(entry[key])
                    else:
                        current_combined[key] = [current_combined[key], entry[key]]
        else:
            combined_entries.append(current_combined)
            current_combined = entry

    if current_combined is not None:
        combined_entries.append(current_combined)

    return combined_entries

def set_tp(symbol, quantity, takeProfit):
    """
    Set a take profit order for a position.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        quantity (float): The quantity to take profit on
        takeProfit (float): The take profit price level
        
    Returns:
        dict: Response from the exchange
        
    Note:
        This function sets a partial take profit, meaning it will only close
        the specified quantity when the take profit level is reached.
    """
    print("SETTING TPSL")
    session = get_bybit_session()
    res = session.set_trading_stop(
        category='linear',
        orderType="Market",
        symbol=symbol,
        tpslMode="Partial",
        takeProfit=float(takeProfit),
        tpSize=str(quantity)
    )
    print(res)
    return res

def get_prices():
    """
    Get current market prices for all open positions.
    
    Returns:
        dict: Dictionary mapping symbols to their current prices
        
    Note:
        This function fetches the latest price for each symbol that has an open position.
    """
    session = get_bybit_session()
    positions_response = session.get_positions(category="linear", settleCoin="USDT")
    positions = positions_response.get('result', {}).get('list', [])
    prices = {}
    
    for position in positions:
        symbol = position.get('symbol')
        price_response = session.get_tickers(category="linear", symbol=symbol)
        price = price_response.get('result', {}).get('list', [])[0]
        prices[symbol] = price['lastPrice']
    
    return prices

def delete_tp_orders(symbol):
    """
    Delete all take profit orders for a specific symbol.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        
    Note:
        This function will only delete orders of type 'PartialTakeProfit'.
    """
    session = get_bybit_session()
    try:
        open_orders = session.get_open_orders(category='linear', symbol=symbol).get('result', {}).get('list', [])
        for order in open_orders:
            if order['stopOrderType'] == 'PartialTakeProfit':
                delete_order(symbol, order['orderId'])
    except Exception as e:
        print(f'Error deleting TP orders: {e}')

def delete_dca_orders(symbol):
    """
    Delete all Dollar Cost Averaging (DCA) orders for a specific symbol.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        
    Note:
        This function will only delete limit orders that are typically used for DCA.
    """
    session = get_bybit_session()
    try:
        open_orders = session.get_open_orders(category='linear', symbol=symbol).get('result', {}).get('list', [])
        for order in open_orders:
            if order['orderType'] == 'Limit':
                delete_order(symbol, order['orderId'])
    except Exception as e:
        print(f'Error deleting DCA orders: {e}')

def delete_all_orders(symbol):
    """
    Delete all open orders for a specific symbol.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        
    Note:
        This function will delete all types of orders (limit, stop loss, take profit).
    """
    session = get_bybit_session()
    try:
        open_orders = session.get_open_orders(category='linear', symbol=symbol).get('result', {}).get('list', [])
        for order in open_orders:
            delete_order(symbol, order['orderId'])
    except Exception as e:
        print(f'Error deleting all orders: {e}')

def delete_order(symbol, orderId):
    """
    Delete a specific order by its ID.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        orderId (str): The unique identifier of the order to delete
    """
    session = get_bybit_session()
    try:
        session.cancel_order(
            category='linear',
            symbol=symbol,
            orderId=orderId
        )
    except Exception as e:
        print(f'Error deleting order: {e}')

def set_max_lev(symbol):
    """
    Set the maximum allowed leverage for a trading symbol.
    
    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSDT')
        
    Note:
        This function sets both buy and sell leverage to 100x, which is the maximum
        allowed by Bybit for most trading pairs.
    """
    session = get_bybit_session()
    try:
        session.set_leverage(
            category='linear',
            symbol=symbol,
            buyLeverage='100',
            sellLeverage='100'
        )
    except Exception as e:
        print(f'Error setting leverage: {e}')
