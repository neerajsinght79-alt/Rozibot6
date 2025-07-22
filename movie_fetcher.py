
from pyrogram import Client
from config import STRING_SESSION, API_ID, API_HASH, MOVIE_SOURCE_BOT

temp_client = Client("fetcher", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

async def fetch_movies(query):
    await temp_client.start()
    bot = await temp_client.get_users(MOVIE_SOURCE_BOT)
    response = await temp_client.send_message(bot.id, query)
    replies = []
    async for msg in temp_client.search_messages(bot.id, query=query, limit=5):
        replies.append(msg)
    await temp_client.stop()
    return replies
