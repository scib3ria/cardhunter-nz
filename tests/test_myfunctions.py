import unittest
from cardhunternz.cardhunternz import CardHunter

class CardHunterTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.cardhunter = CardHunter()

    def test_no_cards(self):
        """Test running cardhunter with no cards specified"""
        self.cardhunter.findCards([])
        self.assertEqual(self.cardhunter.data, )

    def test_one_card(self):
        """Test search one card not contained within a list"""
    
    def test_fake_card(self):
        """Test search for a card that isn't real"""

    def test_card_list(self):
        """Test search for a list of five cards"""
    
    def test_long_list(self):
        """Test search for a list of one hundred cards"""

    def test_cards_mtg(self):
        """Test search for mtg cards with the same name as fab cards"""
    
    def test_cards_fab(self):
        """Test search for fab cards with the same name as mtg cards"""