from fastapi import FastAPI, HTTPException
from typing import List
from contextlib import asynccontextmanager
import asyncio
from .card_hunter import CardHunter
from .models import Card as Card
from .db import Session

# Initialize CardHunter globally
hunter = CardHunter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler: runs at startup and shutdown
    """
    print("[INFO] Fetching all card data...")

    # Run the Shopify scraping asynchronously
    async def startup_scrape():
        # Fetch Shopify stores concurrently
        await hunter.fetch_all_shopify()
        # Fetch Hobbymaster synchronously
        hunter.fetch_hobbymaster()

    try:
        await startup_scrape()
        with Session() as session:
            total = session.query(Card).count()
            print(f"[INFO] Database ready with {total} total cards.")
    except Exception as e:
        print(f"[ERROR] Failed to populate database at startup: {e}")

    yield
    # Optional shutdown logic
    print("[INFO] App shutdown.")

# Create FastAPI app with lifespan handler
app = FastAPI(title="CardHunter API", version="1.0", lifespan=lifespan)


@app.get("/scrape", summary="Scrape all stores and update the database")
def scrape():
    try:
        hunter.fetch_databases()
        return {"status": "success", "message": "Database updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", summary="Search cards by title")
def search(cards: List[str]):
    """
    Search the database by a list of card titles.
    Example: /search?cards=Black Lotus&cards=Lightning Bolt
    """
    results = hunter.search(cards)
    if not results:
        raise HTTPException(status_code=404, detail="No matching cards found.")

    return [
        {
            "store": c.store,
            "game": c.game,
            "title": c.title,
            "variant_title": c.variant_title,
            "price": c.price,
            "quantity": c.quantity,
            "handle": c.handle,
            "link": c.link
        }
        for c in results
    ]
