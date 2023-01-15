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
#               card_name         store                                            version  price
# 8   Crashing Drawbridge   BeaDndGames  Crashing Drawbridge [Throne of Eldraine] - Nea...   0.80
# 11     Famished Paladin  Goblin Games      Famished Paladin [Rivals of Ixalan] - NM-Mint   0.50
# 4   Gremlin Infestation     BayDragon  Gremlin Infestation [Magic the Gathering Aethe...   0.41

# All prices:
#               card_name             store                                            version  price
# 0   Gremlin Infestation       HobbyMaster                             Gremlin Infestation NM   0.50
# 1   Gremlin Infestation       HobbyMaster                      Gremlin Infestation (Foil) NM   1.00
# 2      Famished Paladin       HobbyMaster                                Famished Paladin NM   0.60
# 3   Crashing Drawbridge       HobbyMaster                             Crashing Drawbridge NM   0.90
# 4   Gremlin Infestation         BayDragon  Gremlin Infestation [Magic the Gathering Aethe...   0.41
# 5      Famished Paladin         BayDragon  Famished Paladin [Magic the Gathering Rivals o...   0.56
# 6   Gremlin Infestation       BeaDndGames    Gremlin Infestation [Aether Revolt] - Near Mint   0.50
# 7      Famished Paladin       BeaDndGames    Famished Paladin [Rivals of Ixalan] - Near Mint   0.70
# 8   Crashing Drawbridge       BeaDndGames  Crashing Drawbridge [Throne of Eldraine] - Nea...   0.80
# 9   Crashing Drawbridge     Card Merchant  Crashing Drawbridge [Throne of Eldraine] - Nea...   1.00
# 10  Gremlin Infestation      Goblin Games      Gremlin Infestation [Aether Revolt] - NM-Mint   0.50
# 11     Famished Paladin      Goblin Games      Famished Paladin [Rivals of Ixalan] - NM-Mint   0.50
# 12  Crashing Drawbridge      Goblin Games  Crashing Drawbridge [Throne of Eldraine] - NM-...   1.00
# 13  Crashing Drawbridge      Goblin Games  Crashing Drawbridge [Throne of Eldraine] - NM-...   1.50
# 14  Gremlin Infestation  Spellbound Games      Gremlin Infestation [Aether Revolt] - NM / SP   0.80
# 15  Gremlin Infestation  Spellbound Games  Gremlin Infestation [Aether Revolt] - NM / SP ...   0.80
# 16     Famished Paladin  Spellbound Games      Famished Paladin [Rivals of Ixalan] - NM / SP   0.80
# 17     Famished Paladin  Spellbound Games  Famished Paladin [Rivals of Ixalan] - NM / SP ...   0.80