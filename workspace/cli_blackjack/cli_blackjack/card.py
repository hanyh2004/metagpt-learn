class Card:
    """
    This class represents a card in the game of blackjack.
    Each card has a rank, suit, and value.
    """

    def __init__(self, rank: str, suit: str, value: int):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return self.__str__()

    def get_value(self):
        return self.value
