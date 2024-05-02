import discord
import pymongo
from pymongo import MongoClient
from test import *
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
    if trade_info:
        # Update database and decide if trading should proceed
        update_or_create_trade_signal(trade_info)
        execute_trade(trade_info)

def update_or_create_trade_signal(trade_info):
    """ Updates an existing trade signal or creates a new one if it doesn't exist. """
    query = {'Coin': trade_info['Coin']}
    update = {"$set": trade_info}
    options = True
    collection.update_one(query, update, options)
    print(f"Signal processed for {trade_info['Coin']} - updated or inserted as needed.")

def execute_trade(trade_info):
    """ Logic to execute trade based on updated trade_info """
    print(f"Executing trade for {trade_info['Coin']}")
    execute_trade(trade_info)
    
    # Add your trading logic here, which may involve calling a trading API or executing other actions

# Enter your bot's token here
BOT_TOKEN = 'MTE5NDUxMjc1ODU5OTg1MjA1Mg.GJYbaG._jSuN1noAtO2JOo9ZW8PrEYZBEbadUJImkcrpw'
client.run(BOT_TOKEN)
