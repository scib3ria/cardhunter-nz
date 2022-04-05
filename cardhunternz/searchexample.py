from cardhunternz import CardHunter
import pandas as pd


card_hunter = CardHunter()
cards = [
    "Gremlin Infestation",
    "Famished Paladin",
    "Crashing Drawbridge",
]
prices = []
card_hunter.findCards(cards)

# use card_hunter.summarisePrices().to_csv() for better spreadsheet parsing
print(card_hunter.summarisePrices())

#                      Lowest price Best store(s)   Hobbymaster     BayDragon  BeaDndGames   Calico Keep     Card Bard Card Merchant Card Merchant Nelson  Goblin Games Iron Knight Gaming Magic at Willis Shuffle and Cut Games Spellbound Games
# Gremlin Infestation          0.36     BayDragon           0.5          0.36          0.4  Out of Stock  Out of Stock  Out of Stock         Out of Stock           0.5                0.4    Out of Stock          Out of Stock              0.8
# Famished Paladin             0.40   Hobbymaster           0.4          0.47          0.5  Out of Stock  Out of Stock  Out of Stock         Out of Stock           0.5       Out of Stock    Out of Stock                     1              0.8
# Crashing Drawbridge          0.30  Goblin Games  Out of Stock  Out of Stock          0.6           0.4  Out of Stock  Out of Stock         Out of Stock           0.3       Out of Stock    Out of Stock          Out of Stock     Out of Stock
# Total                        1.06             0           0.9          0.83          1.5           0.4             0             0                    0           1.3                0.4               0                     1              1.6