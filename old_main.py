import discord
from datetime import datetime, timedelta
from bybit_api import *
import asyncio
import datetime

# Bband1 = None
# Bband5 = None
# Bband1_time = None
# Bband5_time = None
# reset_task = None

# async def reset_variables_after_timeout():
#     global Bband1, Bband5, Bband1_time, Bband5_time
#     await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds)

#     # Reset variables if the second one hasn't been updated within 5 minutes
#     if Bband1_time and Bband5_time and (Bband1_time - Bband5_time > datetime.timedelta(minutes=5) or Bband5_time - Bband1_time > datetime.timedelta(minutes=5)):
#         Bband1, Bband5 = None, None
#         Bband1_time, Bband5_time = None, None


account = get_account_value()
print('Account Balance: $',account['totalEquity'])
# Enter your bot's token here
BOT_TOKEN = 'MTE5NDUxMjc1ODU5OTg1MjA1Mg.GJYbaG._jSuN1noAtO2JOo9ZW8PrEYZBEbadUJImkcrpw'
e = False
symbol = 'BTCUSDT'
last_entered_price = 0
side = 'Buy'


#set manually before starting program
intents = discord.Intents.default()
intents.messages = True  # This enables receiving messages
intents.message_content = True  # To access message content


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')



@client.event
async def on_message(message):
    global last_entered_price
    global side
    # Avoid responding to own messages
    if message.author == client.user:
        return
    try:
        signal=str(message.content).split(":")

        positions = get_positions(symbol)
        if(len(positions) > 0):
            if(signal[0] == 'DCA'):
                #DCA
                print('DCA Added')
            elif(signal[0] == 'TP'):
                print('Took TP')
                print('MOVED SL')
            elif(signal[0] == 'SL'):
                print('SL hit, all positions exited')
        else:
            if(signal[0] == 'Entry'):
                side = signal[1]
                #put current price
                last_entered_price = 0
                open_position(signal)
                print('Entered Position')

                print('Added SL')
                
        exit_all_positions()
        open_position(signal)
        add_sl_diff(50)
        
    except Exception as e:
        print(f'Error occurred: {e}')
        exit_all_positions()
        account = get_account_value()
        print('Account Balance: $',account['totalEquity'])
        await client.close()


def add_sl_diff(diff):
    global symbol
    positions = get_positions(symbol)[0]
    if(positions.get('side') == 'Sell'):
        add_sl(symbol, float(positions.get('avgPrice'))+diff)
    else:
        add_sl(symbol, float(positions.get('avgPrice'))-diff)

def set_sl(price):
    global symbol
    add_sl(symbol, float(price))



def exit_all_positions():
    global symbol
    positions = get_positions(symbol)
    size = int(positions[0]['size'])
    side = positions[0]['side']
    if(size > 0):
        if(side == 'Buy'):
            side = 'Sell'
        elif(side == 'Sell'):
            side = 'Buy'
        pnl = float(positions[0]['unrealisedPnl'])
        res = close_market(symbol, size, side)
        print(res)
        #Sell All positions
        print(f"SOLD ALL POSITIONS, PNL:${pnl}")
        account = get_account_value()
        print('Account Balance: $',account['totalEquity'])
    else:
        return


def open_position(signal):
    global symbol
    res = set_market_order(symbol, 1, signal)
    print(res)
    print('Position Added!')       






client.run(BOT_TOKEN)
