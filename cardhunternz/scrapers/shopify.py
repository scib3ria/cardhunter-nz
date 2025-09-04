# scrapers/shopify_scraper.py
import asyncio
import httpx
import pandas as pd
from cardhunternz.store_config import STORE_CONFIG

# 🔒 Global semaphore for ALL Shopify stores
GLOBAL_SHOPIFY_LIMITER = asyncio.Semaphore(2)  # ~2 requests at a time across all stores

class ShopifyScraper:
    def __init__(self, store_name: str):
        self.store_name = store_name
        self.config = STORE_CONFIG[store_name]
        self.base_url = self.config["base_url"]

    async def _fetch_with_retry(self, session: httpx.AsyncClient, url: str, retries=5, base_delay=1):
        """Fetch a URL with retry + exponential backoff + jitter, using global limiter."""
        for attempt in range(retries):
            try:
                async with GLOBAL_SHOPIFY_LIMITER:  # 🔑 Global rate limit
                    resp = await session.get(url, timeout=20)
                if resp.status_code == 429:
                    raise Exception("Rate limited (429)")
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                wait = base_delay * (2 ** attempt) + (0.1 * attempt)
                print(f"[{self.store_name}] Retry {attempt+1}/{retries} for {url} - {e}. Waiting {wait:.1f}s")
                await asyncio.sleep(wait)
        raise Exception(f"[{self.store_name}] Failed after {retries} retries for {url}")

    async def _fetch_products_page(self, session: httpx.AsyncClient, handle: str, page: int):
        url = f"{self.base_url}/collections/{handle}/products.json?page={page}&limit=250"
        return await self._fetch_with_retry(session, url)

    async def scrape_collection(self, session: httpx.AsyncClient, game: str, handle: str):
        """Scrape a single collection (all pages)."""
        all_products = []
        page = 1

        while True:
            data = await self._fetch_products_page(session, handle, page)
            products = data.get("products", [])
            if not products:
                break
            for p in products:
                all_products.append({
                    "store": self.store_name,
                    "game": game,
                    "title": p["title"],
                    "variant_title": ", ".join([v["title"] for v in p.get("variants", []) if v["title"] != "Default Title"]),
                    "price": float(p["variants"][0]["price"]),
                    "quantity": p["variants"][0]["inventory_quantity"],
                    "handle": p["handle"],
                    "link": f"{self.base_url}/products/{p['handle']}"
                })
            page += 1

        return all_products

    async def scrape_all(self):
        """Scrape all collections for this store."""
        tasks = []
        async with httpx.AsyncClient() as session:
            for game, handle in self.config["collections"].items():
                tasks.append(self.scrape_collection(session, game, handle))
            results = await asyncio.gather(*tasks, return_exceptions=True)

        all_cards = []
        for res in results:
            if isinstance(res, Exception):
                print(f"[{self.store_name}] ERROR: {res}")
            else:
                all_cards.extend(res)

        return all_cards
