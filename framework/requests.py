import aiohttp
from os import getenv
from io import BytesIO
# people wanted me to stop using requests
# so i made this fake requests module
# kek

class response:
    def __init__(self, res):
        self.res = res
    
    async def text(self):
        return await self.res.text()
    
    async def json(self):
        return await self.res.json()
    
    async def content(self):
        return await self.res.read()
    
    async def buffer(self):
        result = await self.res.read()
        return BytesIO(result)

class requests:
    def __init__(self):
        self.bot_session = aiohttp.ClientSession()
        self.dbl_session = aiohttp.ClientSession(headers={'Authorization': 'Bearer '+getenv('DBL_TOKEN')})
    
    async def get(self, url, headers=None, timeout=10):
        async with session.get('http://httpbin.org/get') as resp:
        result = await self.session.get(url)