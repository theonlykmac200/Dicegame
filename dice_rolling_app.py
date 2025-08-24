import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict

class DiceRollingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Rolling Game")
        self.root.geometry("800x600")
        
        # Configure root window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Game state
        self.num_players = 1
        self.num_dice = 1
        self.current_player = 0
        self.player_scores = defaultdict(list)
        self.game_started = False
        
        # Create main frames
        self.setup_frame = ttk.Frame(root, padding="20")
        self.setup_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.game_frame = ttk.Frame(root, padding="20")
        
        # Setup UI
        self.create_setup_ui()
        
        # Force update
        self.root.update_idletasks()
        
    def create_setup_ui(self):
        # Title
        title_label = ttk.Label(self.setup_frame, text="Dice Rolling Game", 
                               font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Number of players selection
        ttk.Label(self.setup_frame, text="Number of Players:", 
                 font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        self.players_var = tk.IntVar(value=1)
        players_frame = ttk.Frame(self.setup_frame)
        players_frame.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        for i in range(1, 7):
            ttk.Radiobutton(players_frame, text=str(i), variable=self.players_var, 
                           value=i).pack(side=tk.LEFT, padx=5)
        
        # Number of dice selection
        ttk.Label(self.setup_frame, text="Number of Dice:", 
                 font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.dice_var = tk.IntVar(value=1)
        dice_frame = ttk.Frame(self.setup_frame)
        dice_frame.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        for i in range(1, 7):
            ttk.Radiobutton(dice_frame, text=str(i), variable=self.dice_var, 
                           value=i).pack(side=tk.LEFT, padx=5)
        
        # Start game button
        start_button = ttk.Button(self.setup_frame, text="Start Game", 
                                 command=self.start_game)
        start_button.grid(row=3, column=0, columnspan=2, pady=30)
        
    def create_game_ui(self):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Current player label
        self.current_player_label = ttk.Label(self.game_frame, 
                                            text=f"Player {self.current_player + 1}'s Turn", 
                                            font=('Arial', 18, 'bold'))
        self.current_player_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Dice display frame
        self.dice_frame = ttk.Frame(self.game_frame)
        self.dice_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Roll button
        roll_button = ttk.Button(self.game_frame, text="Roll Dice!", 
                               command=self.roll_dice, 
                               style='Large.TButton')
        roll_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Create custom style for larger button
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 14))
        
        # Score display
        score_frame = ttk.LabelFrame(self.game_frame, text="Scores", padding="10")
        score_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # Create score labels for each player
        self.score_labels = []
        for i in range(self.num_players):
            player_label = ttk.Label(score_frame, text=f"Player {i + 1}:", 
                                   font=('Arial', 10))
            player_label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            
            score_label = ttk.Label(score_frame, text="No rolls yet", 
                                  font=('Arial', 10))
            score_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            self.score_labels.append(score_label)
        
        # Back to setup button
        back_button = ttk.Button(self.game_frame, text="New Game", 
                               command=self.back_to_setup)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)
        
    def start_game(self):
        self.num_players = self.players_var.get()
        self.num_dice = self.dice_var.get()
        self.current_player = 0
        self.player_scores = defaultdict(list)
        self.game_started = True
        
        # Switch to game frame
        self.setup_frame.grid_remove()
        self.game_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create game UI
        self.create_game_ui()
        
    def roll_dice(self):
        # Clear previous dice
        for widget in self.dice_frame.winfo_children():
            widget.destroy()
        
        # Roll dice and display results
        roll_results = []
        for i in range(self.num_dice):
            result = random.randint(1, 6)
            roll_results.append(result)
            
            # Create dice display
            dice_label = tk.Label(self.dice_frame, text=self.get_dice_face(result), 
                                font=('Courier', 40), bg='white', relief=tk.RAISED, 
                                width=3, height=2)
            dice_label.grid(row=0, column=i, padx=5)
        
        # Calculate total
        total = sum(roll_results)
        total_label = ttk.Label(self.dice_frame, 
                              text=f"Total: {total}", 
                              font=('Arial', 16, 'bold'))
        total_label.grid(row=1, column=0, columnspan=self.num_dice, pady=10)
        
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
                score_text = f"Rolls: {rolls[-5:]} | Total: {sum(rolls)} | Avg: {sum(rolls)/len(rolls):.1f}"
                self.score_labels[i].config(text=score_text)
    
    def back_to_setup(self):
        self.game_frame.grid_remove()
        self.setup_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.game_started = False

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollingApp(root)
    root.mainloop()