from cardhunternz import CardHunter
import pandas as pd


card_hunter = CardHunter()
cards = [
    "Gremlin Infestation",
    "Famished Paladin",
]
prices = []
card_hunter.findCards(cards)
print(card_hunter.summarisePrices())


#                         Card  Hobbymaster  Hareruya EN  Hareruya JP  Baydragon  Goblin Games  Spellbound  Magic at Willis  Iron Knight Gaming  Magic Magpie
# 0          Archmage Emeritus         -1.0        10.39         1.30       3.60           2.5         3.0             -1.0                  -1            -1
# 1   Deekah, Fractal Theorist         -1.0        -1.00         3.90       1.66           1.5         2.1             -1.0                  -1            -1
# 2         Chandra's Ignition         -1.0        -1.00         6.49      -1.00          -1.0        -1.0              8.5                  -1            -1
# 3   Veyran, Voice of Duality         -1.0        -1.00        -1.00      21.36          22.0        -1.0             -1.0                  -1            -1
# 4  Zaffir, Thunder Conductor         -1.0        -1.00        -1.00      -1.00          -1.0        -1.0             -1.0                  -1            -1
# 5  Jadzi, Oracle of Arcavios          4.8         6.49        32.47      -1.00           5.0        -1.0             -1.0                  -1            -1
# 6     Octavia, Living Thesis          1.8        -1.00        -1.00       5.22           3.5        -1.0             -1.0                  -1            -1
# 0       Spawnbroker          0.9          3.9         3.90         -1           0.7         1.5              0.7                  -1         -1.00
# 1  Puppeteer Clique         -1.0          2.6         0.65         -1           7.5        -1.0              7.6                  -1          9.55