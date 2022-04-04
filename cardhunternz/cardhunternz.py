import pandas as pd
import requests, time
from bs4 import BeautifulSoup


class CardHunter:
    # List of New Zealand stores selling trading card singles (specifically Magic: the Gathering and Flesh and Blood)
    stores = {
            'Hobbymaster': 'https://hobbymaster.co.nz/cards/get-cards',
            'BayDragon': 'https://www.baydragon.co.nz/search/category/01',
            'Calico Keep': 'calico-keep.myshopify.com',
            'Card Bard': 'cardbard.myshopify.com',
            'Card Merchant': 'chloetest.myshopify.com',
            'Card Merchant Nelson': 'card-merchant-nelson.myshopify.com',
            'Goblin Games': 'goblingames.myshopify.com',
            'Iron Knight Gaming': 'iron-knight-gaming.myshopify.com',
            'Magic at Willis': 'magicatwillis.myshopify.com',
            'Shuffle and Cut Games': 'shuffle-n-cut-hobbies-games.myshopify.com',
            'Spellbound Games': 'spellboundgames.myshopify.com',
        }
    def __init__(self):
        self.data = {}
        # Instantiates a requests session for connecting to store websites
        self.conn = requests.Session()
        # Choose which games you want to search
        self.games = [i for i in ['MTG Single', 'Flesh And Blood Single'] if input(f'Are you searching for {i}s? (y/n): ') == 'y']

    def hobbymasterSearch(self, card_name):
        data = []
        for game in self.games:
            game_number = '1' if game == 'MTG Single' else '37'
            hb_data = self.conn.get(f'https://hobbymaster.co.nz/cards/get-cards?game={game_number}&_search=true&name={card_name}').json()
            if 'rows' in hb_data:
                data.extend(hb_data['rows'])
        # Waits for a second to avoid spamming the Hobbymaster API with too many requests at once
        time.sleep(1)
        return data
    
    def baydragonSearch(self, card_name):
        params = {'searchType': 'single', 'searchString': card_name}
        url = 'https://www.baydragon.co.nz/search/category/01'
        html_content = self.conn.get(self.stores['BayDragon'], params=params).text
        data = BeautifulSoup(html_content, "lxml")
        return data
    
    def shopifySearch(self, card_name, store):
        url = 'https://appbeta.binderpos.com/external/shopify/products/forStore'
        data = {
            'productTypes': self.games,
            'instockOnly': True,
            'storeUrl': self.stores[store],
            'strict': True,
            'limit': 100,
            'title': card_name,
        }
        resp = self.conn.post(url, json=data)
        return resp.json()
    
    def storeSearch(self, card_name, store):
        url = self.stores[store]
        card_results = []
        
        if store == 'Hobbymaster':
            data = self.hobbymasterSearch(card_name)
            # The data from Hobbymaster is stored a little strangely. Each cell is a list containing 12 items related to a card entry
            # The cell[0] is the card name, cell[9] is the card condition, cell[10] is the card price and cell[12] is the card stock
            for result in data:
                if result['cell'][12] != 0:
                    card_results.append({
                        'Name': f'{result["cell"][0]} {result["cell"][9]}',
                        'Price': float(result['cell'][10].replace('$', ''))
                    })
                    
        
        elif store == 'BayDragon':
            if 'MTG Single' not in self.games:
                return card_results
            data = self.baydragonSearch(card_name)
            # HTML parsing of the results table
            div = data.find('div', attrs={'class': 'tcgSingles'})
            table = div.find('table')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                d = [ele.text.strip() for ele in cols if ele]
                # Filters out the column headings and any cards that are out of stock
                if d[7] not in ['Onhand', '0']:
                    card_results.append({
                        'Name': "{} [{}] - {}".format(d[1], d[2], d[5]),
                        'Price': float(d[6].replace('NZ$', ''))
                    })
        
        else:
            # Queries BinderPOS API for each store  and processes the resulting data
            data = self.shopifySearch(card_name, store)
            for product in data['products']:
                if product['overallQuantity']:
                    for variant in product['variants']:
                        if variant['quantity']:
                            card_results.append({
                                'Name': '{} - {}'.format(product["title"], variant["title"]),
                                'Price': variant['price']
                            })

        return card_results
    
    def findCards(self, card_list):
        # Updates the data with each card in card_list containing an empty dict
        self.data.update({k: {} for k in card_list})

        for card_name in self.data.keys():
            for store in self.stores.keys():
                self.data[card_name][store] = self.storeSearch(card_name, store)
    
    def cheapestCard(self, stocklist):
        # Determines what are the cheapest cards from each store
        cheapest_cards = [min([card['Price'] for card in stocklist[store]]) if stocklist[store] else 'Out of Stock' for store in stocklist.keys()]
        # Assigns lowest price and best store if the card is out of stock everywhere
        if list(set(cheapest_cards))[0] == 'Out of Stock':
            lowest_price = 'N/A'
            best_stores = 'Not available'
        # Finds the lowest price out of the cheapest cards from each store
        else:
            lowest_price = min([price for price in cheapest_cards if price != 'Out of Stock'])
            best_stores = '/'.join([store for store, cards in stocklist.items() if any((card['Price'] == lowest_price) for card in cards )])
    
        return lowest_price, best_stores, cheapest_cards
    
    def summarisePrices(self, pandas=True):
        card_dict = {}
        store_list = list(self.stores.keys())
        columns = ['Lowest price', 'Best store(s)'] + store_list
        for card, store_data in self.data.items():
            lowest_price, best_stores, cheapest_cards = self.cheapestCard(store_data)
            card_dict[card] = [lowest_price, best_stores] + cheapest_cards
        card_dict['Total'] = [sum([card_dict[card][i] for card in card_dict.keys() if isinstance(card_dict[card][i], float)]) for i in range(len(store_list) + 2)]
        # By default returns a pandas dataframe with a summary of the card prices
        if pandas:
            summary = pd.DataFrame.from_dict(card_dict, orient='index', columns=columns)
            return summary
        # Optionally, can return a text summary of the results if the dataframe does not display well
        else:
            for card, items in card_dict.items():
                if items[0] == 'N/A':
                    print(f'Though we have searched far and wide, {card} is nowhere to be found in fair New Zealand!')
                elif card == 'Total':
                    print(f'The lowest total cost for these cards (excluding shipping costs) is ${items[0]}')
                else:
                    print(f'{card} is available for ${items[0]} at {items[1]}')
                    print(*(f'  {k} - {v}' for k, v in zip(items[2:], store_list)), sep='\n')