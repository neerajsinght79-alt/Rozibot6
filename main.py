from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION

# Bot client
bot = Client(
    "RoziBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# User client (for forwarding messages from source bot)
user = Client(
    name="userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(bot_client, message: Message):
    await message.reply_text("Rozi bot is alive and ready! 🔥")

@bot.on_message(filters.text & filters.private)
async def forward_handler(bot_client, message: Message):
    if len(message.text) < 3:
        return await message.reply_text("Movie name too short.")
    
    # Search in @Premiummovies0_bot using user client
    async with user:
        sent = await user.send_message("Premiummovies0_bot", message.text)
        await sent.delete()  # Optional: delete search message

        @user.on_message(filters.chat("Premiummovies0_bot"))
        async def handler(_, msg: Message):
            await message.reply_text(msg.text, disable_web_page_preview=True)

# Start both clients
user.start()
bot.run()
