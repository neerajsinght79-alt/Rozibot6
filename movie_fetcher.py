from pyrogram import Client
from config import API_ID, API_HASH, SOURCE_BOT_USERNAME

async def fetch_movie_results(bot_username, query):
    async with Client("movie-fetcher", api_id=API_ID, api_hash=API_HASH, in_memory=True) as app:
        results = []
        async for msg in app.search_messages(bot_username, query, limit=5):
            if msg.text:
                results.append({
                    "title": msg.text.split('\n')[0][:40],
                    "link": f"https://t.me/{bot_username.replace('@','')}/{msg.id}"
                })
        return results
