import asyncio
from typing import List
from scrapers.base import BaseScraper
from progress import ProgressTracker

class Orchestrator:
    def __init__(
        self,
        scrapers: List[BaseScraper],
        batch_handler,
        batch_size: int = 500,
        max_retries: int = 2,
        delay: int = 5,
        progress_file: str = "scrape_progress.json"
    ):
        self.scrapers = scrapers
        self.batch_handler = batch_handler
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.delay = delay
        self.progress = ProgressTracker(progress_file)

    async def _run_scraper(self, scraper: BaseScraper):
        attempt = 0
        store_name = scraper.store_name

        while attempt <= self.max_retries:
            try:
                if hasattr(scraper, "scrape_all_with_progress"):
                    await self._maybe_async(scraper.scrape_all_with_progress, scraper, self.batch_handler, self.batch_size, self.progress)
                elif asyncio.iscoroutinefunction(scraper.scrape_all):
                    await scraper.scrape_all(self.batch_handler, self.batch_size)
                else:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, scraper.scrape_all, self.batch_handler, self.batch_size)

                return
            except Exception as e:
                attempt += 1
                if attempt > self.max_retries:
                    print(f"[ERROR] Scraper {store_name} failed after {self.max_retries} retries: {e}")
                else:
                    print(f"[WARN] Scraper {store_name} failed on attempt {attempt}, retrying in {self.delay}s: {e}")
                    await asyncio.sleep(self.delay)

    async def _maybe_async(self, func, scraper, batch_handler, batch_size, progress):
        if asyncio.iscoroutinefunction(func):
            await func(batch_handler, batch_size, progress)
        else:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, func, batch_handler, batch_size, progress)

    async def run_all(self):
        tasks = [self._run_scraper(scraper) for scraper in self.scrapers]
        await asyncio.gather(*tasks)
