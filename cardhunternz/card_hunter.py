import asyncio
import pandas as pd
from typing import List
from .scrapers.shopify import ShopifyScraper
from .scrapers.hobbymaster import HobbymasterScraper
from .store_config import STORE_CONFIG
from .db import Session, init_db
from .models import Card

class CardHunter:
    def __init__(self):
        init_db()

    def save_cards(self, cards: list[dict]):
        with Session() as session:
            for card in cards:
                db_card = Card(**card)
                session.add(db_card)
            session.commit()

    async def fetch_shopify_store(self, store_name: str):
        scraper = ShopifyScraper(store_name)
        cards = await scraper.scrape_all()

        if cards:
            print(f"[i] Found {len(cards)} cards for {store_name}")
            self.save_cards(cards)
        print(f"[✓] Finished fetching {store_name}")


    async def fetch_all_shopify(self):
        tasks = []
        for store_name in STORE_CONFIG.keys():
            tasks.append(self.fetch_shopify_store(store_name))
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for res in results:
            if isinstance(res, Exception):
                print(f"[ERROR] {res}")
            elif isinstance(res, pd.DataFrame) and not res.empty:
                self.save_cards(res.to_dict(orient="records"))

    def fetch_hobbymaster(self):
        scraper = HobbymasterScraper()
        cards = scraper.scrape_all()
        if cards:
            print(f"[i] Found {len(cards)} cards for Hobbymaster")
            self.save_cards(cards)
        print("[✓] Finished fetching Hobbymaster")

    def fetch_databases(self):
        """Fetch all stores and save to database."""
        # Shopify async scraping
        asyncio.run(self.fetch_all_shopify())

        # Hobbymaster synchronous scraping
        self.fetch_hobbymaster()

        with Session() as session:
            total = session.query(Card).count()
            print(f"[✓] Database updated with {total} total cards")

    def search(self, card_list: list[str]):
        with Session() as session:
            results = (
                session.query(Card)
                .filter(Card.title.in_(card_list))
                .order_by(Card.title, Card.price)
                .all()
            )
            return results