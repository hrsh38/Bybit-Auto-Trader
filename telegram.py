from telethon import TelegramClient, events, sync
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Telegram credentials from environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
error_id = int(os.getenv('TELEGRAM_ERROR_CHAT_ID', -2069690427))

# The name of the session file (to save your login session, so you don't need to log in every time)
session_file = 'my_telegram_session'

def create_telegram_client():
    """Create and return a Telegram client instance."""
    if not api_id or not api_hash:
        raise ValueError("Telegram API credentials not found in environment variables")
    
    return TelegramClient(session_file, api_id, api_hash)

client = create_telegram_client()

@client.on(events.NewMessage())
async def my_event_handler(event):
    """Handle new messages in Telegram."""
    print("h", type(event.chat_id), event.chat_id, event.peer_id)
    if event.chat_id == error_id:
        print("Error:", event.raw_text)

def start_telegram_client():
    """Start the Telegram client."""
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    start_telegram_client()