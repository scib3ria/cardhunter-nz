from abc import ABC, abstractmethod
import pandas as pd
import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar

class CardStore(ABC):
    def __init__(self, url, name, games, skip_art_cards=True):
        self.url = url
        self.name = name
        self.games = games
        self.skip_art_cards=skip_art_cards
        self.conn = requests.Session()
        self.data = {}

    def findCards(self, card_list):
        # Updates the data with each card in card_list containing an empty dict
        self.data.update({k: {} for k in card_list})

        with alive_bar(len(self.data.keys()), dual_line=True, title=self.name, title_length=21) as bar:
            for card_name in self.data.keys():
                bar.text = f'Hunting for {card_name}'
                self.data[card_name] = self.storeSearch(card_name)
                bar()
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
                    'price': variant['Price'],
                    'quantity': variant['Quantity']
                }
                flat_list.append(flat_json)
        df = pd.DataFrame.from_records(flat_list)
        return df

class ShopifyStore(CardStore):
    # Queries BinderPOS API for each store  and processes the resulting data
    def storeSearch(self, card_name):
        card_results = []
        data = {
            'productTypes': self.games,
            'instockOnly': True,
            'storeUrl': self.url,
            'strict': True,
            'limit': 100,
            'title': card_name,
            'quantityGreaterThan': 0,
        }
        resp = self.conn.post(url = 'https://portal.binderpos.com/external/shopify/products/forStore', json=data).json()

        for product in resp['products']:
                if product['overallQuantity']:
                    for variant in product['variants']:
                        if variant['quantity'] > 0:
                            # skip art cards
                            if ("art card" in product["title"].lower()) and self.skip_art_cards:
                                continue
                            card_results.append({
                                'Name': '{} - {}'.format(product["title"], variant["title"]),
                                'Price': variant['price'],
                                'Quantity': variant['quantity']
                            })
        return card_results

class HobbyMasterStore(CardStore):
    def storeSearch(self, card_name):
        card_results = []
        data = []
        for game in self.games:
            game_number = '1' if game == 'MTG Single' else '37'
            hb_data = self.conn.get(f'{self.url}?lang=&game={game_number}$foil=&_search=true&name={card_name}').json()
            if 'rows' in hb_data:
                data.extend(hb_data['rows'])
        # The data from Hobbymaster is stored a little strangely. Each cell is a list containing 12 items related to a card entry
        # The cell[0] is the card name, cell[9] is the card condition, cell[10] is the card price and cell[12] is the card stock
        for result in data:
            if result['cell'][12] != 0:
                # replace '8+' string with int
                quantity = result['cell'][12]
                if quantity == '8+': quantity = 8
                # skip art cards
                if ("art card" in result["cell"][0].lower()) and self.skip_art_cards:
                            continue
                card_results.append({
                    'Name': f'{result["cell"][0]} [{result["cell"][1]}] {result["cell"][9]}',
                    'Price': float(result['cell'][10].replace('$', '')),
                    'Quantity': quantity
                })
        return card_results
    
class BayDragonStore(CardStore):
    def storeSearch(self, card_name):
        card_results = []
        # baydragon does not currently sell Flesh and Blood singles
        game_number = '01' if 'MTG Single' in self.games else '25'
        params = {'searchType': 'single', 'searchString': card_name}
        html_content = self.conn.get(f'{self.url}/brand/{game_number}', params=params).text
        data = BeautifulSoup(html_content, "lxml")
        # HTML parsing of the results table
        table = data.find('table', attrs={'id': ['tcgSingles', 'magicSingles']})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            d = [ele.text.strip() for ele in cols if ele]
            # Filters out the column headings and any cards that are out of stock
            if d[7] not in ['Onhand', '0']:

                # skip art cards
                if ("art card" in d[1].lower()) and self.skip_art_cards:
                    continue

                card_results.append({
                    'Name': "{} [{}] - {}".format(d[1], d[2], d[5]),
                    'Price': float(d[6].replace('NZ$', '')),
                    'Quantity': d[7]
                })
        return card_results

class RookGamingStore(CardStore):
    def storeSearch(self, card_name):
        # Rook Gaming does not currently sell MTG singles
        card_results = []
        if 'Flesh And Blood Single' not in self.games:
            return card_results        
        html_content = self.conn.get(f'{self.url}/search?q={card_name}').text
        data = BeautifulSoup(html_content, "lxml")
        # HTML parsing of the results
        search_results = data.find('div', attrs={'class': 'template-search__results'})
        product_cards = search_results.find_all('div', attrs={'class': 'product-card product-grid'})
        for product_card in product_cards:
            # Skip cards that are out of stock
            if product_card.find('span', attrs = {'class': 'label-sold-out'}):
                continue
            card_results.append({
                'Name': product_card.find('h6', attrs = {'class': 'product-card__name'}).text.strip('\n'),
                'Price': float(product_card.find('div', attrs = {'class': 'product-price'}).text.strip('$')),
                'Quantity': 1 # Rook Gaming does not have card quantities on its results page
            })
        return card_results
    
class FabArmoryStore(CardStore):
    def storeSearch(self, card_name):
        # Fabarmory does not currently sell MTG singles
        card_results = []
        if 'Flesh And Blood Single' not in self.games:
            return card_results
        html_content = self.conn.get(f'{self.url}/search?q={card_name}').text
        data = BeautifulSoup(html_content, "lxml")
        items = data.find('ul', attrs= {'class': 'page-width list-view-items'})
        card_products = items.find_all('li')
        for card_product in card_products:
            # Skip cards that are not in stock
            if card_product.find('dl', attrs={'class': 'price--sold-out'}):
                continue
            card_results.append({
                'Name': card_product.find('span', attrs={'class': 'product-card__title'}).text,
                'Price': float(card_product.find('span', attrs={'class': 'price-item--regular'}).text.strip('$').strip()),
                'Quantity': 1, # FAB Armory does not have card quantities on its results page
            })
        return card_results