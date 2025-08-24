import tkinter as tk
from tkinter import ttk
import random
from collections import defaultdict

class DiceRollingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Rolling Game")
        self.root.geometry("800x600")
        
        # Game state
        self.num_players = 1
        self.num_dice = 1
        self.current_player = 0
        self.player_scores = defaultdict(list)
        self.game_started = False
        
        # Create main container
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create setup frame
        self.setup_frame = tk.Frame(self.main_container)
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create game frame (hidden initially)
        self.game_frame = tk.Frame(self.main_container)
        
        # Setup UI
        self.create_setup_ui()
        
    def create_setup_ui(self):
        # Title
        title_label = tk.Label(self.setup_frame, text="Dice Rolling Game", 
                               font=('Arial', 24, 'bold'))
        title_label.pack(pady=20)
        
        # Number of players selection
        players_label = tk.Label(self.setup_frame, text="Number of Players:", 
                                font=('Arial', 12))
        players_label.pack(pady=10)
        
        self.players_var = tk.IntVar(value=1)
        players_frame = tk.Frame(self.setup_frame)
        players_frame.pack(pady=10)
        
        for i in range(1, 7):
            tk.Radiobutton(players_frame, text=str(i), variable=self.players_var, 
                          value=i, font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Number of dice selection
        dice_label = tk.Label(self.setup_frame, text="Number of Dice:", 
                             font=('Arial', 12))
        dice_label.pack(pady=10)
        
        self.dice_var = tk.IntVar(value=1)
        dice_frame = tk.Frame(self.setup_frame)
        dice_frame.pack(pady=10)
        
        for i in range(1, 7):
            tk.Radiobutton(dice_frame, text=str(i), variable=self.dice_var, 
                          value=i, font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Start game button
        start_button = tk.Button(self.setup_frame, text="Start Game", 
                                command=self.start_game, font=('Arial', 14),
                                bg='green', fg='white', padx=20, pady=10)
        start_button.pack(pady=30)
        
    def create_game_ui(self):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Current player label
        self.current_player_label = tk.Label(self.game_frame, 
                                           text=f"Player {self.current_player + 1}'s Turn", 
                                           font=('Arial', 18, 'bold'))
        self.current_player_label.pack(pady=20)
        
        # Dice display frame
        self.dice_display_frame = tk.Frame(self.game_frame)
        self.dice_display_frame.pack(pady=20)
        
        # Roll button
        roll_button = tk.Button(self.game_frame, text="Roll Dice!", 
                               command=self.roll_dice, 
                               font=('Arial', 16),
                               bg='blue', fg='white', padx=30, pady=15)
        roll_button.pack(pady=20)
        
        # Score display
        score_label = tk.Label(self.game_frame, text="Scores", 
                              font=('Arial', 14, 'bold'))
        score_label.pack(pady=10)
        
        self.score_frame = tk.Frame(self.game_frame)
        self.score_frame.pack(pady=10)
        
        # Create score labels for each player
        self.score_labels = []
        for i in range(self.num_players):
            player_frame = tk.Frame(self.score_frame)
            player_frame.pack(anchor=tk.W, pady=2)
            
            player_label = tk.Label(player_frame, text=f"Player {i + 1}:", 
                                   font=('Arial', 10), width=10, anchor=tk.W)
            player_label.pack(side=tk.LEFT)
            
            score_label = tk.Label(player_frame, text="No rolls yet", 
                                  font=('Arial', 10), anchor=tk.W)
            score_label.pack(side=tk.LEFT)
            self.score_labels.append(score_label)
        
        # Back to setup button
        back_button = tk.Button(self.game_frame, text="New Game", 
                               command=self.back_to_setup,
                               font=('Arial', 12))
        back_button.pack(pady=20)
        
    def start_game(self):
        self.num_players = self.players_var.get()
        self.num_dice = self.dice_var.get()
        self.current_player = 0
        self.player_scores = defaultdict(list)
        self.game_started = True
        
        # Switch to game frame
        self.setup_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create game UI
        self.create_game_ui()
        
    def roll_dice(self):
        # Clear previous dice
        for widget in self.dice_display_frame.winfo_children():
            widget.destroy()
        
        # Roll dice and display results
        roll_results = []
        dice_frame = tk.Frame(self.dice_display_frame)
        dice_frame.pack()
        
        for i in range(self.num_dice):
            result = random.randint(1, 6)
            roll_results.append(result)
            
            # Create dice display
            dice_label = tk.Label(dice_frame, text=self.get_dice_face(result), 
                                font=('Courier', 40), bg='white', relief=tk.RAISED, 
                                width=3, height=2)
            dice_label.pack(side=tk.LEFT, padx=5)
        
        # Calculate total
        total = sum(roll_results)
        total_label = tk.Label(self.dice_display_frame, 
                              text=f"Total: {total}", 
                              font=('Arial', 16, 'bold'))
        total_label.pack(pady=10)
        
        # Update player scores
        self.player_scores[self.current_player].append(total)
        self.update_scores()
        
        # Move to next player
        self.current_player = (self.current_player + 1) % self.num_players
        self.current_player_label.config(text=f"Player {self.current_player + 1}'s Turn")
        
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
    
    def update_scores(self):
        for i in range(self.num_players):
            if i in self.player_scores and self.player_scores[i]:
                rolls = self.player_scores[i]
                last_rolls = rolls[-5:] if len(rolls) > 5 else rolls
                score_text = f"Rolls: {last_rolls} | Total: {sum(rolls)} | Avg: {sum(rolls)/len(rolls):.1f}"
                self.score_labels[i].config(text=score_text)
    
    def back_to_setup(self):
        self.game_frame.pack_forget()
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        self.game_started = False

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollingApp(root)
    root.mainloop()