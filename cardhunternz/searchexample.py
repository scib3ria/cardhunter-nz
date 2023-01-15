from cardhunternz import CardHunter
import pandas as pd


card_hunter = CardHunter()
cards = [
    "Gremlin Infestation",
    "Famished Paladin",
    "Crashing Drawbridge"
]
prices = []
card_hunter.findCards(cards)

# use card_hunter.allPrices().to_csv() for better spreadsheet parsing
print("Cheapest prices:")
print(card_hunter.cheapestPrices())
print("\nAll prices:")
print(card_hunter.allPrices())

# Cheapest prices:
#               card_name         store                                            version  price quantity
# 8   Crashing Drawbridge   BeaDndGames  Crashing Drawbridge [Throne of Eldraine] - Nea...   0.80       33
# 10     Famished Paladin  Goblin Games      Famished Paladin [Rivals of Ixalan] - NM-Mint   0.50        7
# 4   Gremlin Infestation     BayDragon  Gremlin Infestation [Magic the Gathering Aethe...   0.41        3

# All prices:
#               card_name             store                                            version  price quantity
# 8   Crashing Drawbridge       BeaDndGames  Crashing Drawbridge [Throne of Eldraine] - Nea...   0.80       33
# 3   Crashing Drawbridge       HobbyMaster                             Crashing Drawbridge NM   0.90        3
# 11  Crashing Drawbridge      Goblin Games  Crashing Drawbridge [Throne of Eldraine] - NM-...   1.00        7
# 12  Crashing Drawbridge      Goblin Games  Crashing Drawbridge [Throne of Eldraine] - NM-...   1.50        1
# 10     Famished Paladin      Goblin Games      Famished Paladin [Rivals of Ixalan] - NM-Mint   0.50        7
# 5      Famished Paladin         BayDragon  Famished Paladin [Magic the Gathering Rivals o...   0.56        3
# 2      Famished Paladin       HobbyMaster                                Famished Paladin NM   0.60        2
# 7      Famished Paladin       BeaDndGames    Famished Paladin [Rivals of Ixalan] - Near Mint   0.70        1
# 15     Famished Paladin  Spellbound Games      Famished Paladin [Rivals of Ixalan] - NM / SP   0.80        7
# 16     Famished Paladin  Spellbound Games  Famished Paladin [Rivals of Ixalan] - NM / SP ...   0.80        1
# 4   Gremlin Infestation         BayDragon  Gremlin Infestation [Magic the Gathering Aethe...   0.41        3
# 0   Gremlin Infestation       HobbyMaster                             Gremlin Infestation NM   0.50        8
# 6   Gremlin Infestation       BeaDndGames    Gremlin Infestation [Aether Revolt] - Near Mint   0.50       17
# 9   Gremlin Infestation      Goblin Games      Gremlin Infestation [Aether Revolt] - NM-Mint   0.50       16
# 13  Gremlin Infestation  Spellbound Games      Gremlin Infestation [Aether Revolt] - NM / SP   0.80       11
# 14  Gremlin Infestation  Spellbound Games  Gremlin Infestation [Aether Revolt] - NM / SP ...   0.80        1
# 1   Gremlin Infestation       HobbyMaster                      Gremlin Infestation (Foil) NM   1.00        2