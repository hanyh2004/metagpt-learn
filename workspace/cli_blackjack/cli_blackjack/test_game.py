import unittest
from game import Game
from player import Player
from card import Card

class TestGame(unittest.TestCase):
    def setUp(self):
        self.dealer = Player()
        self.player = Player()
        self.players = [self.dealer, self.player]
        self.game = Game(self.players)

    def test_start_game(self):
        self.game.start_game()
        self.assertEqual(len(self.dealer.get_hand()), 2)
        self.assertEqual(len(self.player.get_hand()), 2)

    def test_deal_card(self):
        self.game.start_game()
        self.game.deal_card(self.player)
        self.assertEqual(len(self.player.get_hand()), 3)

    def test_check_winner(self):
        self.dealer.hit(Card('A', 'Hearts', 11))
        self.dealer.hit(Card('K', 'Hearts', 10))
        self.player.hit(Card('2', 'Hearts', 2))
        self.player.hit(Card('3', 'Hearts', 3))
        self.assertEqual(self.game.check_winner(), self.dealer)

if __name__ == '__main__':
    unittest.main()
