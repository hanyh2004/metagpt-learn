import random
from typing import List
from player import Player
from card import Card

class Game:
    """
    This class represents a game of blackjack.
    The game has a list of players, a deck of cards, and methods to start the game, deal a card, and check the winner.
    """

    def __init__(self, players: List[Player]):
        self.players = players
        self.deck = self._create_deck()

    def _create_deck(self) -> List[Card]:
        """
        Creates a deck of 52 cards.
        """
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        deck = [Card(rank, suit, values[rank]) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def start_game(self):
        """
        Starts the game by dealing two cards to each player.
        """
        for _ in range(2):
            for player in self.players:
                self.deal_card(player)

    def deal_card(self, player: Player):
        """
        Deals a card to a player.
        The card is removed from the deck and added to the player's hand.
        """
        card = self.deck.pop()
        player.hit(card)

    def check_winner(self) -> Player:
        """
        Checks the winner of the game.
        The player with the highest score not exceeding 21 is the winner.
        If there is a tie, the dealer wins.
        """
        dealer = self.players[0]
        winner = dealer
        for player in self.players[1:]:
            if player.get_score() > winner.get_score() and player.get_score() <= 21:
                winner = player
        return winner
