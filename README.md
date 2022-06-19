# cardhunter-nz
A python library for finding the best prices on trading cards singles from stores in New Zealand. 
Currently works for Magic: the Gathering and Flesh and Blood cards.
Searches the following stores:
- Hobbymaster
- BayDragon
- BeaDndGames
- Calico Keep
- Card Bard
- Card Merchant
- Card Merchant Nelson
- Goblin Games
- Iron Knight Gaming
- Magic at Willis
- Shuffle and Cut Games
- Spellbound Games
- TCG Culture

# Instructions

Instantiate the cardhunter like so:

```cardhunter = CardHunter()```

This will create a cardhunter object that will prompt you as to which card games you would like to search for (currently Magic: the Gathering and Flesh and Blood). Enter y or n at each prompt.

Search for cards like so:

```
card_list = [
  'counterspell',
  'lightning bolt',
  'black lotus',
  ...
]
cardhunter.findCards(card_list)
```

The cardhunter will take some time to retrieve and process the data.

Once finished, call `cardhunter.summarisePrices()` to display a summary of the card prices in a pandas dataframe. You may also call `cardhunter.summarisePrices(pandas=False)` to display a text summary of the card prices if you would prefer.

# Requirements

Using python3

```pip install -r requirements.txt```

Use a virtual environment first

```
python3 -m venv .venv
. .venv/bin/activate
```
