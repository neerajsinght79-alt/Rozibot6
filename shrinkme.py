import aiohttp
from config import SHRINKME_API_KEY

async def create_shortlink(original_url, user_id):
    api_url = f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={original_url}&alias=user{user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()
            return data.get("shortenedUrl") or original_url
