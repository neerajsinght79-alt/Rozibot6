import aiohttp
from config import SHRINKME_API_KEY

async def get_shortlink(url):
    api_url = f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()
            return data.get("shortenedUrl", url)
