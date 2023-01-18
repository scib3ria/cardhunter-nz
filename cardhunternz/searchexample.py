from cardhunternz import CardHunter
import pandas as pd


card_hunter = CardHunter(mtg_search=True)
cards = [
    "Gremlin Infestation",
    "Famished Paladin",
    "Crashing Drawbridge"
]
prices = []
card_hunter.findCards(cards)

# turn off pandas max rows
pd.set_option("display.max_rows", None)
print("Cheapest prices:")
print(card_hunter.cheapestPrices())
print("\nAll prices:")
print(card_hunter.allPrices())
# use card_hunter.allPrices().to_csv() for better spreadsheet parsing

# Cheapest prices:
#               card_name         store                                            version  price quantity
# 0   Crashing Drawbridge   HobbyMaster                             Crashing Drawbridge NM   0.80        3
# 4      Famished Paladin  Goblin Games      Famished Paladin [Rivals of Ixalan] - NM-Mint   0.50        7
# 10  Gremlin Infestation     BayDragon  Gremlin Infestation [Magic the Gathering Aethe...   0.41        3

# All prices:
#               card_name             store                                            version  price quantity
# 0   Crashing Drawbridge       HobbyMaster                             Crashing Drawbridge NM   0.80        3
# 1   Crashing Drawbridge       BeaDndGames  Crashing Drawbridge [Throne of Eldraine] - Nea...   0.80       33
# 2   Crashing Drawbridge      Goblin Games  Crashing Drawbridge [Throne of Eldraine] - NM-...   1.00        7
# 3   Crashing Drawbridge      Goblin Games  Crashing Drawbridge [Throne of Eldraine] - NM-...   1.50        1
# 4      Famished Paladin      Goblin Games      Famished Paladin [Rivals of Ixalan] - NM-Mint   0.50        7
# 5      Famished Paladin         BayDragon  Famished Paladin [Magic the Gathering Rivals o...   0.56        3
# 6      Famished Paladin       HobbyMaster                                Famished Paladin NM   0.60        2
# 7      Famished Paladin       BeaDndGames    Famished Paladin [Rivals of Ixalan] - Near Mint   0.70        1
# 8      Famished Paladin  Spellbound Games      Famished Paladin [Rivals of Ixalan] - NM / SP   0.80        7
# 9      Famished Paladin  Spellbound Games  Famished Paladin [Rivals of Ixalan] - NM / SP ...   0.80        1
# 10  Gremlin Infestation         BayDragon  Gremlin Infestation [Magic the Gathering Aethe...   0.41        3
# 11  Gremlin Infestation       HobbyMaster                             Gremlin Infestation NM   0.50        8
# 12  Gremlin Infestation       BeaDndGames    Gremlin Infestation [Aether Revolt] - Near Mint   0.50       17
# 13  Gremlin Infestation      Goblin Games      Gremlin Infestation [Aether Revolt] - NM-Mint   0.50       16
# 14  Gremlin Infestation  Spellbound Games      Gremlin Infestation [Aether Revolt] - NM / SP   0.80       11
# 15  Gremlin Infestation  Spellbound Games  Gremlin Infestation [Aether Revolt] - NM / SP ...   0.80        1
# 16  Gremlin Infestation       HobbyMaster                      Gremlin Infestation (Foil) NM   1.00        2