import pandas as pd
import requests
from cardstore import (
    BayDragonStore,
    FabArmoryStore,
    HobbyMasterStore,
    RookGamingStore,
    ShopifyStore
)
class CardHunter:
    # List of New Zealand stores selling trading card singles (specifically Magic: the Gathering and Flesh and Blood)
    
    store_data = {
        'HobbyMaster': {
            'type': 'hobbymaster',
            'url': 'https://hobbymaster.co.nz/cards/get-cards',
            'products': ['MTG Single', 'Flesh And Blood Single', 'One Piece Single']
        },
        'BayDragon': {
            'type': 'baydragon',
            'url': 'https://www.baydragon.co.nz/search/category/01',
            'products': ['MTG Single', 'Flesh And Blood Single', 'One Piece Single']
        },
        'BeaDndGames': {
            'type': 'shopify',
            'url': 'bea-dnd.myshopify.com',
            'products': ['MTG Single', 'Star Wars: Unlimited Single']
        },
        'Calico Keep': {
            'type': 'shopify',
            'url': 'calico-keep.myshopify.com',
            'products': ['MTG Single']
        },
        'Card Bard': {
            'type': 'shopify',
            'url': 'cardbard.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single']
        },
        'Card Merchant': {
            'type': 'shopify',
            'url': 'chloetest.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'Star Wars: Unlimited Single']
        },
        'Card Merchant Christchurch': {
            'type': 'shopify',
            'url': 'card-merchant-christchurch.myshopify.com',
            'products': ['MTG Single', 'One Piece Single']
        },
        'Card Merchant Hamilton': {
            'type': 'shopify',
            'url': 'card-merchant-hamilton.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'Grand Archive Single', 'One Piece Single', 'Star Wars: Unlimited Single']
        },
        'Card Merchant Nelson': {
            'type': 'shopify',
            'url': 'card-merchant-nelson.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'Grand Archive Single', 'One Piece Single']
        },
        'Card Merchant Takapuna': {
            'type': 'shopify',
            'url': 'kidsandmore.myshopify.com',
            'products': ['MTG Single', 'Grand Archive Single', 'One Piece Single']
        },
        'Card Merchant Whangarei': {
            'type': 'shopify',
            'url': 'cardmerchantwhangarei.myshopify.com',
            'products': ['MTG Single', 'Grand Archive Single']
        },
        'Fabarmory': {
            'type': 'fabarmory',
            'url': 'https://fabarmoury-com.myshopify.com',
            'products': ['Flesh And Blood Single']
        },
        'Gaming DNA': {
            'type': 'shopify',
            'url': 'gaming-dna.myshopify.com',
            'products': ['MTG Single']
        },
        'Goblin Games': {
            'type': 'shopify',
            'url': 'goblingames.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'One Piece Single', 'Star Wars: Unlimited Single']
        },
        'Iron Knight Gaming': {
            'type': 'shopify',
            'url': 'iron-knight-gaming.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'Star Wars: Unlimited Single']
        },
        'Magic at Willis': {
            'type': 'shopify',
            'url': 'magicatwillis.myshopify.com',
            'products': ['MTG Single']
        },
        'Nova Games': {
            'type': 'shopify',
            'url': 'novagames-nz.myshopify.com',
            'products': ['MTG Single']
        },
        'Rook Gaming': {
            'type': 'rookgaming',
            'url': 'https://e734ef.myshopify.com',
            'products': ['Flesh And Blood Single']
        },
        'Shuffle and Cut Games': {
            'type': 'shopify',
            'url': 'shuffle-n-cut-hobbies-games.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'One Piece Single']
        },
        'Spellbound Games': {
            'type': 'shopify',
            'url': 'spellboundgames.myshopify.com',
            'products': ['MTG Single', 'One Piece Single', 'Star Wars: Unlimited Single']
        },
        'TCG Collector': {
            'type': 'shopify',
            'url': 'tcg-collector-nz.myshopify.com',
            'products': ['MTG Single', 'Grand Archive Single', 'One Piece Single', 'Star Wars: Unlimited Single']
        },
        'TCG Culture': {
            'type': 'shopify',
            'url': 'tcgculture.myshopify.com',
            'products': ['Flesh And Blood Single', 'One Piece Single']
        },
        'XP Games': {
            'type': 'shopify',
            'url': 'xp-games-ltd.myshopify.com',
            'products': ['MTG Single', 'Flesh And Blood Single', 'Grand Archive Single', 'One Piece Single']
        }
    }
    
    def __init__(self, mtg_search=False, fab_search=False, ga_search=False, op_search=False, swu_search=False):
        self.data = pd.DataFrame()
        # Instantiates a requests session for connecting to store websites
        self.conn = requests.Session()
        self.games = []
        if mtg_search: 
            self.games.append('MTG Single')
        if fab_search: 
            self.games.append('Flesh And Blood Single')
        if ga_search: 
            self.games.append('Grand Archive Single')
        if op_search: 
            self.games.append('One Piece Single')
        if swu_search: 
            self.games.append('Star Wars: Unlimited Single')
        # Choose which games you want to search if no default set
        single_types = [
            'MTG Single', 
            'Flesh And Blood Single',
            'Grand Archive Single',
            'One Piece Single',
            'Star Wars: Unlimited Single'                
        ]
        if not self.games:
            self.games = [i for i in single_types if input(f'Are you searching for {i}s? (y/n): ') == 'y']
        self._get_stores()
        
    def _get_stores(self):
        
        self.stores = []
        for store_name, store_info in self.store_data.items():
            # Checks whether any of the games selected are in the store's listed products
            if set(self.games) & set(store_info['products']):
                if store_info['type'] == 'hobbymaster':
                    self.stores.append(HobbyMasterStore(url=store_info['url'], name=store_name, games=self.games))
                elif store_info['type'] == 'baydragon':
                    self.stores.append(BayDragonStore(url=store_info['url'], name=store_name, games=self.games))
                elif store_info['type'] == 'fabarmory':
                    self.stores.append(FabArmoryStore(url=store_info['url'], name=store_name, games=self.games))
                elif store_info['type'] == 'rookgaming':
                    self.stores.append(RookGamingStore(url=store_info['url'], name=store_name, games=self.games))
                else:
                    self.stores.append(ShopifyStore(url=store_info['url'], name=store_name, games=self.games))
    
    def findCards(self, card_list):
        # Updates the data with search results from each store
        results = []
        for store in self.stores:
            store.findCards(card_list)
            results.append(store.get_dataframe())
        self.data = pd.concat(results, ignore_index=True)
        # Checks if self.data dataframe has data in it
        if self.data.empty:
            for card in card_list:
                print(f'Though we have searched far and wide, {card} is nowhere to be found in fair New Zealand!')
        else:
            self.data = self.data.sort_values(by=['card_name', 'price']).reset_index(drop=True)
            for card in card_list:
                if card not in list(self.data['card_name'].unique()):
                    print(f'Though we have searched far and wide, {card} is nowhere to be found in fair New Zealand!')
    
    def cheapestPrices(self, pandas=True):
        cheapest_cards = self.data.loc[self.data.groupby('card_name')['price'].idxmin(), :]
        if pandas:
            return cheapest_cards
        else:
            return f"""{cheapest_cards.to_string()}

The lowest total cost for these cards (excluding shipping costs) is ${cheapest_cards['price'].sum()}"""

    def allPrices(self):
        return self.data