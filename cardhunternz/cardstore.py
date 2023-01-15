from abc import ABC, abstractmethod
import pandas as pd
import requests
import time
import json
from bs4 import BeautifulSoup

class CardStore(ABC):
    def __init__(self, url, name, games):
        self.url = url
        self.name = name
        self.games = games
        self.conn = requests.Session()
        self.data = {}

    def findCards(self, card_list):
        # Updates the data with each card in card_list containing an empty dict
        self.data.update({k: {} for k in card_list})

        for card_name in self.data.keys():
            searchTime = time.time()
            self.data[card_name] = self.storeSearch(card_name)
            print(f"Searching {self.name} for {card_name} took {time.time()-searchTime:.2f} seconds")
        return self.data

    @abstractmethod
    def storeSearch(self, card_name):
        pass

    def get_dataframe(self):
        flat_list = []
        for search_name, stock in self.data.items():
            for variant in stock:
                flat_json = {
                    'card_name': search_name,
                    'store': self.name,
                    'version': variant['Name'],
                    'price': variant['Price']
                }
                flat_list.append(flat_json)
        df = pd.DataFrame.from_records(flat_list)
        return df

class ShopifyStore(CardStore):

    def storeSearch(self, card_name):
        card_results = []
        data = {
            'productTypes': self.games,
            'instockOnly': True,
            'storeUrl': self.url,
            'strict': True,
            'limit': 100,
            'title': card_name,
        }
        resp = self.conn.post(url = 'https://appbeta.binderpos.com/external/shopify/products/forStore', json=data).json()

        for product in resp['products']:
                if product['overallQuantity']:
                    for variant in product['variants']:
                        # print(variant)
                        if variant['quantity']:
                            # print(variant)
                            card_results.append({
                                'Name': '{} - {}'.format(product["title"], variant["title"]),
                                'Price': variant['price'],
                            })
        # print(card_results)
        return card_results

class HobbyMasterStore(CardStore):
    def storeSearch(self, card_name):
        card_results = []
        data = []
        for game in self.games:
            game_number = '1' if game == 'MTG Single' else '37'
            hb_data = self.conn.get(f'https://hobbymaster.co.nz/cards/get-cards?lang=&game={game_number}$foil=&_search=true&name={card_name}').json()
            # print(hb_data)
            if 'rows' in hb_data:
                data.extend(hb_data['rows'])
        for result in data:
                if result['cell'][12] != 0:
                    card_results.append({
                        'Name': f'{result["cell"][0]} {result["cell"][9]}',
                        'Price': float(result['cell'][10].replace('$', ''))
                    })
        return card_results
    
class BayDragonStore(CardStore):
    def storeSearch(self, card_name):
        card_results = []
        if 'MTG Single' not in self.games:
                return card_results
        params = {'searchType': 'single', 'searchString': card_name}
        url = 'https://www.baydragon.co.nz/search/category/01'
        html_content = self.conn.get(url, params=params).text
        data = BeautifulSoup(html_content, "lxml")
        # HTML parsing of the results table
        div = data.find('div', attrs={'class': 'tcgSingles'})
        table = div.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            d = [ele.text.strip() for ele in cols if ele]
            # print(d)
            # Filters out the column headings and any cards that are out of stock
            if d[7] not in ['Onhand', '0']:
                card_results.append({
                    'Name': "{} [{}] - {}".format(d[1], d[2], d[5]),
                    'Price': float(d[6].replace('NZ$', ''))
                })
        return card_results


if __name__ == "__main__":
    beadnd = ShopifyStore(url = 'bea-dnd.myshopify.com', name = 'BeaDndGames', games = ['MTG Single'])
    hobbyMaster = HobbyMasterStore(url = 'https://hobbymaster.co.nz/cards/get-cards', name = 'Hobbymaster', games = ['MTG Single'])
    bayDragon = BayDragonStore(url = 'https://www.baydragon.co.nz/search/category/01', name = 'BayDragon', games = ['MTG Single'])
    # print(json.dumps(beadnd.findCards(['island']), indent=2))
    print(json.dumps(beadnd.findCards(['Den of the bugbear']), indent=2))
    print(beadnd.get_dataframe())