import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import *
from movie_fetcher import fetch_movies
from shrinkme import get_shortlink
from helper import save_user_step, get_user_step, force_join_keyboard

app = Client("rozi", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def is_joined(client, user_id):
    try:
        member = await client.get_chat_member(UPDATES_CHANNEL, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    if not await is_joined(client, message.from_user.id):
        await message.reply("🔐 Please join our updates channel to use this bot.", reply_markup=force_join_keyboard())
        return
    await message.reply("👋 Welcome to Rozi Movie Bot!\n\nSend me a movie name to search.")

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def search_movie(client, message: Message):
    if not await is_joined(client, message.from_user.id):
        await message.reply("🔐 Please join our updates channel to use this bot.", reply_markup=force_join_keyboard())
        return

    results = await fetch_movies(message.text)
    if not results:
        await message.reply("❌ No results found.")
        return

    buttons = []
    for i, msg in enumerate(results, 1):
        save_user_step(message.from_user.id, msg.id)
        buttons.append([InlineKeyboardButton(f"{i}. {msg.text[:30]}", callback_data=f"getlink_{msg.id}")])

    await message.reply("🎬 Select a movie to get the download link:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("getlink_"))
async def generate_link(client, callback_query: CallbackQuery):
    msg_id = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    short_url = await get_shortlink(f"https://t.me/{app.me.username}?start=verify_{msg_id}")
    await callback_query.message.reply(
        "🔗 Click below to verify and get your movie:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Get Link", url=short_url)]])
    )

@app.on_message(filters.command("start") & filters.regex("start verify_"))
async def deliver_movie(client, message: Message):
    msg_id = int(message.text.split("_")[1])
    if not await is_joined(client, message.from_user.id):
        await message.reply("🔐 Please join our updates channel to use this bot.", reply_markup=force_join_keyboard())
        return

    try:
        await client.copy_message(chat_id=message.chat.id, from_chat_id=MOVIE_SOURCE_BOT, message_id=msg_id)
    except:
        await message.reply("❌ Failed to deliver the movie. Try again later.")

@app.on_callback_query(filters.regex("verify_join"))
async def joined_check(client, callback_query: CallbackQuery):
    if await is_joined(client, callback_query.from_user.id):
        await callback_query.message.edit("✅ Verified! Now send me a movie name.")
    else:
        await callback_query.answer("❌ You must join the channel first!", show_alert=True)

app.run()
