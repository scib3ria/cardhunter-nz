import pandas as pd
import requests
from cardstore import ShopifyStore, HobbyMasterStore, BayDragonStore

class CardHunter:
    # List of New Zealand stores selling trading card singles (specifically Magic: the Gathering and Flesh and Blood)
    
    def __init__(self):
        self.data = pd.DataFrame()
        # Instantiates a requests session for connecting to store websites
        self.conn = requests.Session()
        # Choose which games you want to search
        self.games = [i for i in ['MTG Single', 'Flesh And Blood Single'] if input(f'Are you searching for {i}s? (y/n): ') == 'y']
        self.stores = [
            HobbyMasterStore(url='https://hobbymaster.co.nz/cards/get-cards', name='HobbyMaster', games=self.games),
            BayDragonStore(url = 'https://www.baydragon.co.nz/search/category/01', name='BayDragon', games=self.games),
            ShopifyStore(url='bea-dnd.myshopify.com', name='BeaDndGames', games=self.games),
            ShopifyStore(url='calico-keep.myshopify.com', name='Calico Keep', games=self.games),
            ShopifyStore(url='cardbard.myshopify.com', name='Card Bard', games=self.games),
            ShopifyStore(url='chloetest.myshopify.com', name='Card Merchant', games=self.games),
            ShopifyStore(url='card-merchant-nelson.myshopify.com', name='Card Merchant Nelson', games=self.games),
            ShopifyStore(url='goblingames.myshopify.com', name='Goblin Games', games=self.games),
            ShopifyStore(url='iron-knight-gaming.myshopify.com', name='Iron Knight Gaming', games=self.games),
            ShopifyStore(url='magicatwillis.myshopify.com', name='Magic at Willis', games=self.games),
            ShopifyStore(url='shuffle-n-cut-hobbies-games.myshopify.com', name='Shuffle and Cut Games', games=self.games),
            ShopifyStore(url='spellboundgames.myshopify.com', name='Spellbound Games', games=self.games),
            ShopifyStore(url='tcgculture.myshopify.com', name='TCG Culture', games=self.games),
        ]
    
    def findCards(self, card_list):
        # Updates the data with search results from each store
        results = []
        for store in self.stores:
            store.findCards(card_list)
            results.append(store.get_dataframe())
        self.data = pd.concat(results, ignore_index=True)
        for card in card_list:
            if card not in list(self.data['card_name'].unique()):
                print(f'Though we have searched far and wide, {card} is nowhere to be found in fair New Zealand!')
    
    def cheapestPrices(self):
        return self.data.loc[self.data.groupby('card_name')['price'].idxmin(), :]

    def allPrices(self):
        return self.data
