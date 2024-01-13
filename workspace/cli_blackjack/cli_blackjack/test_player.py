import unittest
from player import Player
from card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.card1 = Card('A', 'Hearts', 11)
        self.card2 = Card('2', 'Hearts', 2)

    def test_hit(self):
        self.player.hit(self.card1)
        self.assertEqual(self.player.get_score(), 11)
        self.assertEqual(self.player.get_hand(), [self.card1])
        self.player.hit(self.card2)
        self.assertEqual(self.player.get_score(), 13)
        self.assertEqual(self.player.get_hand(), [self.card1, self.card2])

    def test_stand(self):
        self.player.stand()
        self.assertEqual(self.player.get_score(), 0)
        self.assertEqual(self.player.get_hand(), [])

    def test_get_score(self):
        self.player.hit(self.card1)
        self.assertEqual(self.player.get_score(), 11)
        self.player.hit(self.card2)
        self.assertEqual(self.player.get_score(), 13)

    def test_get_hand(self):
        self.player.hit(self.card1)
        self.assertEqual(self.player.get_hand(), [self.card1])
        self.player.hit(self.card2)
        self.assertEqual(self.player.get_hand(), [self.card1, self.card2])

if __name__ == '__main__':
    unittest.main()
