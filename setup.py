from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A library for finding the best prices on trading cards from stores in New Zealand.'
LONG_DESCRIPTION = """
A library for finding the best prices on trading cards from stores in New Zealand. 
Currently works for Magic: the Gathering and Flesh and Blood cards.
Searches the following stores:
Hobbymaster
BayDragon
Calico Keep
Card Bard
Card Merchant
Card Merchant Nelson
Goblin Games
Iron Knight Gaming
Magic at Willis
Shuffle and Cut Games
Spellbound Games
"""

setup(
    name='cardhunternz',
    packages=find_packages(include=['cardhunternz']),
    author='scib3ria',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license='MIT',
    install_requires=['bs4', 'pandas', 'alive_progress'],
)