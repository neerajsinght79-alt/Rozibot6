from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import API_ID, API_HASH, BOT_TOKEN, SOURCE_BOT_USERNAME
from movie_fetcher import fetch_movie_results
from shrinkme import create_shortlink
from helper import save_user_step, get_user_step, clear_user_step

bot = Client("RoziMovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_private(client, message):
    await message.reply_text("👋 Welcome to Rozi Movie Bot!\n\nSearch movies in the group, then click the button to verify and get the link.")

@bot.on_message(filters.text & filters.group)
async def group_movie_search(client, message):
    query = message.text.strip()
    results = await fetch_movie_results(SOURCE_BOT_USERNAME, query)
    if not results:
        await message.reply("❌ No results found.")
        return
    
    buttons = []
    for i, result in enumerate(results, start=1):
        buttons.append([InlineKeyboardButton(f"{i}. {result['title']}", callback_data=f"movie_{i}")])
    
    save_user_step(message.from_user.id, results)
    await message.reply("🎬 Select the movie:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex("movie_"))
async def movie_selected(client, callback_query):
    user_id = callback_query.from_user.id
    results = get_user_step(user_id)
    if not results:
        await callback_query.answer("❌ Session expired. Search again.", show_alert=True)
        return

    index = int(callback_query.data.split("_")[1]) - 1
    if index >= len(results):
        await callback_query.answer("❌ Invalid selection.", show_alert=True)
        return

    selected = results[index]
    shortlink = await create_shortlink(selected['link'], user_id)
    await callback_query.message.reply(
        f"🔗 Click below to verify and get the movie:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Verify via Shortlink", url=shortlink)]
        ])
    )
    clear_user_step(user_id)

bot.run()
