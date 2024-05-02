import re

def extract_info(text):
    data = {}

    # # Extracting coin name
    # coin_match = re.search(r"🪙 Coin: (\w+)", text)
    # if coin_match:
    #     data['Coin'] = coin_match.group(1)

    # # Extracting direction
    # direction_match = re.search(r"📈 Direction: ([\w\s]+)", text)
    # if direction_match:
    #     data['Direction'] = direction_match.group(1).strip()

    # # Extracting entry zone
    # entry_zone_match = re.search(r"💎 Entry Zone: ([\d\.]+) to ([\d\.]+)", text)
    # if entry_zone_match:
    #     data['Entry Zone'] = (entry_zone_match.group(1), entry_zone_match.group(2))

    # # Extracting stop loss
    # stop_loss_match = re.search(r"🔴 Stop Loss: ([\d\.]+)", text)
    # if stop_loss_match:
    #     data['Stop Loss'] = stop_loss_match.group(1)

    # # Extracting take profit numbers
    # tp_matches = re.findall(r"🟢 TP\d+: ([\d\.]+)", text)
    # data['TP'] = {f"{i+1}": value for i, value in enumerate(tp_matches)}

    # return data
    coin_name = re.search(r"🪙 Coin: (\w+)", text).group(1)
    direction = re.search(r"📈 Direction: ([\w\s]+)", text).group(1).strip()
    # leverage = re.search(r"⚔️  Leverage (\d+x to \d+x)", text).group(1)
    entry_zone_match = re.search(r"💎 Entry Zone: ([\d\.]+) to ([\d\.]+)", text)
    if entry_zone_match:
        entry_zone = (float(entry_zone_match.group(1)), float(entry_zone_match.group(2)))
    stop_loss = re.search(r"🔴 Stop Loss: ([\d.]+)", text).group(1)
    risk_level = re.search(r"and Risk level - (\w+)", text).group(1)

        # Extracting take profit levels
    tp_matches = re.findall(r"🟢 TP\d+: ([\d\.]+)", text)
    take_profits = {f"{i+1}": float(value) for i, value in enumerate(tp_matches)}

    # Compiling extracted data into a dictionary
    trade_info = {
        "Coin": coin_name,
        "Direction": direction,
        # "Leverage": leverage,
        "Entry Zone": entry_zone,
        "Stop Loss": float(stop_loss),
        "Risk Level": risk_level,
        "TP": take_profits
    }
    return trade_info


