import httpx
import asyncio

from singleton import SingletonMeta


class WikiSearchAPI(metaclass=SingletonMeta):
    BASE_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def search(self, query: str):
        await asyncio.sleep(5)

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
        }

        response = await self.client.get(self.BASE_URL, params=params)

        return response.json()
