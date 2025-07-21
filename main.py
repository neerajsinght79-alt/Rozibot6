# main.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pyrogram Client
client = Client(
    name="rozibot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    session_string=STRING_SESSION
)

# /start command handler
@client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    await message.reply_text(
        "👋 Hello! I am Rozi Movie Bot.\n\n"
        "🎬 Send a movie name here or search in the group.\n"
        "I'll help you get the download link after verification ✅"
    )

# Text message handler (optional placeholder for now)
@client.on_message(filters.text & filters.private)
async def handle_text(client, message: Message):
    await message.reply_text("🔍 Searching for your movie...\n(Feature under development)")

# Start the bot
if __name__ == "__main__":
    logger.info("🔥 Rozi Bot is starting...")
    client.run()
