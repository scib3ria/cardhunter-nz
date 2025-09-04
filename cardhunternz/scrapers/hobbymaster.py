import requests
from .base import BaseScraper
from ..utils import clean_price, clean_quantity,retry_sync

class HobbymasterScraper(BaseScraper):
    GAME_DICT = {
        "Magic: The Gathering": "1",
        "Yu-Gi-Oh! TCG": "3",
        "Pokemon TCG": "4",
        "Flesh and Blood": "37",
        "One Piece TCG": "54",
        "Disney Lorcana TCG": "61"
    }

    def __init__(self):
        super().__init__("Hobbymaster", "https://hobbymaster.co.nz/cards/get-cards")

    @retry_sync(max_attempts=5, backoff_factor=2)
    def _fetch_data(self, game_code: str):
        url = (
            f"{self.base_url}?lang=&game={game_code}&foil=&_search=false&nd=1742720954757"
            "&rows=20000&page=1&sidx=stock&sord=desc"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def scrape_all(self):
        """Scrape all supported games and yield Card objects in batches."""
        all_cards = []
        for game, game_code in self.GAME_DICT.items():
            try:
                data = self._fetch_data(game_code)
                cards = []
                for row in data.get("rows", []):
                    cell = row.get("cell", {})
                    try:
                        quantity = clean_quantity(cell[12])
                        price = clean_price(cell[10])
                    except Exception:
                        continue
                        print("error!")
                
                    if quantity <= 0 or price is None:
                        continue
                    
                    name = cell[0].rsplit("(", 1)[0].strip()
                    variant_title = f"{cell[0]} [{cell[1]}] ({cell[9]})"
                    link = f"https://hobbymaster.co.nz/cards/card/{cell[17]}"
                
                    cards.append(
                        {
                            "store": "Hobbymaster",
                            "game": game,
                            "title": name,
                            "variant_title": variant_title,
                            "price": price,
                            "quantity": quantity,
                            "handle": "",
                            "link": link
                        }
                    )
                all_cards.extend(cards)
            except Exception as e:
                print(f"[{self.store_name}] Failed to scrape game {game}: {e}")
        return all_cards
