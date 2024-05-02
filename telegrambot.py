import asyncio
from telethon.sync import TelegramClient
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
username = os.getenv("TELEGRAM_USERNAME")

def sendMessage(message, photo_path=None):
    # Manually create a new event loop for the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient('session_name', api_id, api_hash) as client:
        if photo_path and os.path.exists(photo_path):
            try:
                # Send the photo with caption
                client.send_file(username, file=photo_path, caption=message)
                os.remove(photo_path)  # Optionally remove the photo after sending
            except Exception as e:
                print("Error sending photo:", e)
        else:
            try:
                # Send a plain message
                client.send_message(username, message)
            except Exception as e:
                print(f"Error sending message to {username}:", e)

    loop.close()  # Close the event loop after operations

if __name__ == "__main__":
    sendMessage("This is a photo caption.", "./photo.png")
