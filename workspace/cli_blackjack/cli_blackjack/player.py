from typing import List
from card import Card

class Player:
    """
    This class represents a player in the game of blackjack.
    Each player has a hand of cards and a score.
    """

    def __init__(self):
        self.hand: List[Card] = []
        self.score: int = 0

    def hit(self, card: Card):
        """
        The player chooses to take another card.
        The card is added to the player's hand and the player's score is updated.
        """
        self.hand.append(card)
        self.score += card.get_value()

    def stand(self):
        """
        The player chooses to not take any more cards.
        """
        pass

    def get_score(self) -> int:
        """
        Returns the current score of the player.
        """
        return self.score

    def get_hand(self) -> List[Card]:
        """
        Returns the current hand of the player.
        """
        return self.hand
