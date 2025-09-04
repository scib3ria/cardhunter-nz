# batch_handler.py
from typing import List
from models import Card
import sqlite3

DB_FILE = "db/card_data.db"

def init_db():
    """Create the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            name TEXT,
            set_name TEXT,
            rarity TEXT,
            price REAL,
            store TEXT,
            link TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_batch(cards: List[Card]):
    """Insert a batch of cards into the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    card_tuples = [
        (card.name, card.set_name, card.rarity, card.price, card.store, card.link)
        for card in cards
    ]
    
    c.executemany('''
        INSERT INTO cards (name, set_name, rarity, price, store, link)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', card_tuples)

    conn.commit()
    conn.close()


def handle_batch(cards: List[Card]):
    """Main batch handler function passed to orchestrator."""
    if not cards:
        return
    insert_batch(cards)
    print(f"Inserted batch of {len(cards)} cards into DB.")
