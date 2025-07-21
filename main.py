from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION
from helper import save_user_step, get_user_step, clear_user_step
from shrinkme import create_shortlink
from movie_fetcher import fetch_movies

app = Client("RoziBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text(
        f"Hi {message.from_user.first_name},\nI'm Rozi Movie Bot 🍿.\n\nSearch for a movie by name and I’ll help you get it!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Search Movie", switch_inline_query_current_chat="")]
        ])
    )

# Handle inline queries
@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    query = inline_query.query.strip()
    if not query:
        return

    results = await fetch_movies(query)
    await inline_query.answer(results, cache_time=1)

# Callback query for "Get Link"
@app.on_callback_query(filters.regex("getlink_"))
async def get_link(client, callback_query):
    movie_info = callback_query.data.split("getlink_")[1]
    user_id = callback_query.from_user.id

    # Save step to track which movie user selected
    save_user_step(user_id, movie_info)

    short_url = create_shortlink(f"https://t.me/{app.me.username}?start=verify")
    await callback_query.message.reply_text(
        f"🔗 Please verify by clicking the link below:\n{short_url}\n\nAfter that, come back here.",
        disable_web_page_preview=True
    )

# After shortlink verification
@app.on_message(filters.command("verify") & filters.private)
async def verify(client, message: Message):
    user_id = message.from_user.id
    movie_info = get_user_step(user_id)

    if not movie_info:
        await message.reply_text("❌ No movie selected. Please search again.")
        return

    # Deliver the movie
    try:
        await message.reply_text(f"🎬 Here is your movie:\n\n{movie_info}")
    except Exception as e:
        await message.reply_text("⚠️ Error while sending the movie.")
        print(e)

    clear_user_step(user_id)

app.run()
