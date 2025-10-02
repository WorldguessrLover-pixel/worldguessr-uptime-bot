import os
import telegram

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # tu peux définir le chat_id dans Render aussi

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_message(message: str):
    if not CHAT_ID:
        raise ValueError("CHAT_ID is not set in environment variables.")
    bot.send_message(chat_id=CHAT_ID, text=message)
