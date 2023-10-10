import pandas as pd
import requests
from .cardstore import ShopifyStore, HobbyMasterStore, BayDragonStore, RookGamingStore, FabArmoryStore

class CardHunter:
    # List of New Zealand stores selling trading card singles (specifically Magic: the Gathering and Flesh and Blood)
    
    def __init__(self, mtg_search=False, fab_search=False):
        self.data = pd.DataFrame()
        # Instantiates a requests session for connecting to store websites
        self.conn = requests.Session()
        self.games = []
        if mtg_search: self.games.append('MTG Single')
        if fab_search: self.games.append('Flesh And Blood Single')
        # Choose which games you want to search if no default set
        if not self.games:
            self.games = [i for i in ['MTG Single', 'Flesh And Blood Single'] if input(f'Are you searching for {i}s? (y/n): ') == 'y']
        self.stores = [
            BayDragonStore(url='https://www.baydragon.co.nz/searchsingle/category/01', name='BayDragon', games=self.games),
            ShopifyStore(url='bea-dnd.myshopify.com', name='BeaDndGames', games=self.games),
            ShopifyStore(url='calico-keep.myshopify.com', name='Calico Keep', games=self.games),
            ShopifyStore(url='cardbard.myshopify.com', name='Card Bard', games=self.games),
            ShopifyStore(url='chloetest.myshopify.com', name='Card Merchant', games=self.games),
            ShopifyStore(url='card-merchant-christchurch.myshopify.com', name='Card Merchant Christchurch', games=self.games),
            ShopifyStore(url='card-merchant-hamilton.myshopify.com', name='Card Merchant Hamilton', games=self.games),
            ShopifyStore(url='card-merchant-nelson.myshopify.com', name='Card Merchant Nelson', games=self.games),
            ShopifyStore(url='kidsandmore.myshopify.com', name='Card Merchant Takapuna', games=self.games),
            ShopifyStore(url='card-merchant-tauranga.myshopify.com', name='Card Merchant Tauranga', games=self.games),
            FabArmoryStore(url='https://fabarmoury-com.myshopify.com', name='fabarmory.com', games=self.games),
            ShopifyStore(url='goblingames.myshopify.com', name='Goblin Games', games=self.games),
            HobbyMasterStore(url='https://hobbymaster.co.nz/cards/get-cards', name='HobbyMaster', games=self.games),
            ShopifyStore(url='iron-knight-gaming.myshopify.com', name='Iron Knight Gaming', games=self.games),
            ShopifyStore(url='magicatwillis.myshopify.com', name='Magic at Willis', games=self.games),
            ShopifyStore(url='novagames-nz.myshopify.com', name='Nova Games', games=self.games),
            RookGamingStore(url='https://e734ef.myshopify.com', name='Rook Gaming', games=self.games),
            ShopifyStore(url='shuffle-n-cut-hobbies-games.myshopify.com', name='Shuffle and Cut Games', games=self.games),
            ShopifyStore(url='spellboundgames.myshopify.com', name='Spellbound Games', games=self.games),
            ShopifyStore(url='tcg-collector-nz.myshopify.com', name='TCG Collector', games=self.games),
            ShopifyStore(url='tcgculture.myshopify.com', name='TCG Culture', games=self.games),
        ]
    
    def findCards(self, card_list):
        # Updates the data with search results from each store
        results = []
        for store in self.stores:
            store.findCards(card_list)
            results.append(store.get_dataframe())
        self.data = pd.concat(results, ignore_index=True).sort_values(by=['card_name', 'price']).reset_index(drop=True)
    
    def cheapestPrices(self, pandas=True):
        cheapest_cards = self.data.loc[self.data.groupby('card_name')['price'].idxmin(), :]
        if pandas:
            return cheapest_cards
        else:
            return f"""{cheapest_cards.to_string()}

The lowest total cost for these cards (excluding shipping costs) is ${cheapest_cards['price'].sum()}"""

    def allPrices(self):
        return self.data
