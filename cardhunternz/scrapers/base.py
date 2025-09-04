import httpx
import asyncio
from ..models import Card
from ..utils import clean_price, clean_quantity

class BaseScraper:
    def __init__(self, store_name, base_url):
        self.store_name = store_name
        self.base_url = base_url.rstrip("/")

    async def fetch_json(self, client: httpx.AsyncClient, url: str):
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

    async def scrape_all(self):
        raise NotImplementedError
