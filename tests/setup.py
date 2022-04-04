from setuptools import find_packages, setup

setup(
    name='cardhunternz',
    packages=find_packages(include=['cardhunternz']),
    version='0.1.0',
    description='A library for finding the best prices on trading cards from stores in New Zealand.',
    long_description=
    """
    A library for finding the best prices on trading cards from stores in New Zealand. 
    Currently works for Magic: the Gathering and Flesh and Blood cards.
    Searches the following stores:
    Calico Keep
    Card Bard
    Card Merchant
    Card Merchant Nelson
    Dice Jar Games
    Goblin Games
    Hobbymaster
    Shuffle and Cut Games
    """,
    author='scib3ria',
    license='MIT',
    install_requires=['bs4', 'pandas'],
    setup_requires=['pytest-runner'],
    test_require=['pytest==4.4.1'],
    test_suite='tests',
)