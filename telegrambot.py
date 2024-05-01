from telegram import Bot
from telegram.error import TelegramError
import asyncio

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from the .env file into the environment

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in the environment.")


bot = Bot(token=TELEGRAM_TOKEN)

async def send_alert(message: str):
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, bot.send_message, TELEGRAM_CHAT_ID, message)
    except TelegramError as e:
        print(f"Error sending message: {e}")

def sendMessage(message: str):
    asyncio.run(send_alert(message))



# Example usage
if __name__ == "__main__":
    message_content = "Hello, Telegram! This is a test message from my bot."
    sendMessage(message_content)
