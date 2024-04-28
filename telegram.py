from telethon import TelegramClient, events, sync

# Use your own values from my.telegram.org

api_id = '12510265'
api_hash = "9a2309a0a34b0c8d9eee2ce409e4a30a"

# The name of the session file (to save your login session, so you don't need to log in every time)
session_file = 'my_telegram_session'

client = TelegramClient(session_file, api_id, api_hash)
error_id = -2069690427

@client.on(events.NewMessage())
async def my_event_handler(event):
    print("h", type(event.chat_id), event.chat_id, event.peer_id)
    if(event.chat_id == error_id):
        print("Error:", event.raw_text)
    

client.start()
client.run_until_disconnected()