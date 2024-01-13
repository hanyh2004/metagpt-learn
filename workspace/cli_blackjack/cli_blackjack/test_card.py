import unittest
from card import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card('A', 'Hearts', 11)

    def test_str(self):
        self.assertEqual(str(self.card), 'A of Hearts')

    def test_repr(self):
        self.assertEqual(repr(self.card), 'A of Hearts')

    def test_get_value(self):
        self.assertEqual(self.card.get_value(), 11)

if __name__ == '__main__':
    unittest.main()
