import re

def extract_info(text):
    data = {}

    # Extracting coin name
    coin_match = re.search(r"🪙 Coin: (\w+)", text)
    if coin_match:
        data['Coin'] = coin_match.group(1)

    # Extracting direction
    direction_match = re.search(r"📈 Direction: ([\w\s]+)", text)
    if direction_match:
        data['Direction'] = direction_match.group(1).strip()

    # Extracting entry zone
    entry_zone_match = re.search(r"💎 Entry Zone: ([\d\.]+) to ([\d\.]+)", text)
    if entry_zone_match:
        data['Entry Zone'] = (entry_zone_match.group(1), entry_zone_match.group(2))

    # Extracting stop loss
    stop_loss_match = re.search(r"🔴 Stop Loss: ([\d\.]+)", text)
    if stop_loss_match:
        data['Stop Loss'] = stop_loss_match.group(1)

    # Extracting take profit numbers
    tp_matches = re.findall(r"🟢 TP\d+: ([\d\.]+)", text)
    data['Take Profits'] = {f"TP{i+1}": value for i, value in enumerate(tp_matches)}

    return data
text = """
🪙 Coin: PENDLE
📈 Direction: Short
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
# p = extract_info(text)
# print(p)