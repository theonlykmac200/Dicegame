import random
from collections import defaultdict

class DiceRollingGame:
    def __init__(self):
        self.num_players = 1
        self.num_dice = 1
        self.player_scores = defaultdict(list)
        self.current_player = 0
        
    def get_dice_face(self, value):
        dice_faces = {
            1: "⚀",
            2: "⚁", 
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }
        return dice_faces.get(value, str(value))
    
    def display_menu(self):
        print("\n" + "="*40)
        print("      DICE ROLLING GAME")
        print("="*40)
        print("\n1. Start New Game")
        print("2. Exit")
        return input("\nChoose an option (1-2): ")
    
    def setup_game(self):
        print("\n--- Game Setup ---")
        
        # Get number of players
        while True:
            try:
                self.num_players = int(input("Number of players (1-6): "))
                if 1 <= self.num_players <= 6:
                    break
                print("Please enter a number between 1 and 6")
            except ValueError:
                print("Please enter a valid number")
        
        # Get number of dice
        while True:
            try:
                self.num_dice = int(input("Number of dice (1-6): "))
                if 1 <= self.num_dice <= 6:
                    break
                print("Please enter a number between 1 and 6")
            except ValueError:
                print("Please enter a valid number")
        
        # Reset game state
        self.player_scores = defaultdict(list)
        self.current_player = 0
        print(f"\nGame started with {self.num_players} players and {self.num_dice} dice!")
    
    def roll_dice(self):
        print(f"\n--- Player {self.current_player + 1}'s Turn ---")
        input("Press Enter to roll the dice...")
        
        rolls = []
        print("\nRolling...")
        for i in range(self.num_dice):
            result = random.randint(1, 6)
            rolls.append(result)
            print(f"Die {i+1}: {self.get_dice_face(result)}  ({result})")
        
        total = sum(rolls)
        print(f"\nTotal: {total}")
        
        # Update scores
        self.player_scores[self.current_player].append(total)
        
        # Move to next player
        self.current_player = (self.current_player + 1) % self.num_players
    
    def display_scores(self):
        print("\n--- Current Scores ---")
        for i in range(self.num_players):
            if i in self.player_scores and self.player_scores[i]:
                rolls = self.player_scores[i]
                total = sum(rolls)
                avg = total / len(rolls)
                last_5 = rolls[-5:] if len(rolls) > 5 else rolls
                print(f"Player {i+1}: Last rolls: {last_5} | Total: {total} | Average: {avg:.1f}")
            else:
                print(f"Player {i+1}: No rolls yet")
    
    def play_game(self):
        while True:
            self.roll_dice()
            self.display_scores()
            
            print("\n1. Continue rolling")
            print("2. Back to main menu")
            choice = input("\nChoose an option (1-2): ")
            
            if choice == "2":
                break
    
    def run(self):
        print("Welcome to the Dice Rolling Game!")
        
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.setup_game()
                self.play_game()
            elif choice == "2":
                print("\nThanks for playing! Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    game = DiceRollingGame()
    game.run()