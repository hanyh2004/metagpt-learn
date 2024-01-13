from game import Game
from player import Player

def main():
    """
    Main entry of the program.
    Creates a game and players, starts the game, and ends the game.
    """

    # Create a dealer and a player
    dealer = Player()
    player = Player()
    players = [dealer, player]

    # Create a game
    game = Game(players)

    # Start the game
    game.start_game()

    # Game loop
    while True:
        # Show the player's hand and score
        print(f"Your hand: {player.get_hand()}")
        print(f"Your score: {player.get_score()}")

        # Ask the player to hit or stand
        action = input("Do you want to hit or stand? ")

        if action.lower() == "hit":
            game.deal_card(player)
        elif action.lower() == "stand":
            break
        else:
            print("Invalid action. Please enter 'hit' or 'stand'.")

    # Show the dealer's hand and score
    print(f"Dealer's hand: {dealer.get_hand()}")
    print(f"Dealer's score: {dealer.get_score()}")

    # Check the winner
    winner = game.check_winner()
    if winner == player:
        print("You win!")
    else:
        print("Dealer wins.")

if __name__ == "__main__":
    main()
