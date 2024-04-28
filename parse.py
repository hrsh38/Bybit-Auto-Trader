import discord
from test import *

# Enter your bot's token here
BOT_TOKEN = 'MTE5NDUxMjc1ODU5OTg1MjA1Mg.GJYbaG._jSuN1noAtO2JOo9ZW8PrEYZBEbadUJImkcrpw'

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

    # Avoid responding to own messages
    if message.author == client.user:
        return
    
    trade = extract_info(message.content)
    
    print(trade)
       






client.run(BOT_TOKEN)
