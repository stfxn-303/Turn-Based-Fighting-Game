import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from datetime import datetime
from battlegame import Game, build_team
from tkinter import ttk
import random

STARTING_HP = 100

class GameGUI:
    def __init__(self, root, game_instance):
        self.root = root
        self.game = game_instance
        self.attacker_index = None
        self.target_index = None
        self.event_log = []
        
        # Setup the GUI and buttons
        self.setup_gui()
        self.create_buttons()

        # Prompt for player names after setting up the GUI
        self.prompt_player_names()

    def setup_gui(self):
        self.root.title("Battle Game Interface")
        self.root.configure(bg="#0b0c3e")  # Dark blue background

        # Main frame to contain everything, with a dark blue background
        self.main_frame = tk.Frame(self.root, bg="#0b0c3e")
        self.main_frame.pack(fill="both", expand=True)

        # Background canvas for stars
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600, bg="#0b0c3e", highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.draw_starry_sky()  # Draw stars on the background

        # Player, AI, and log frames
        self.game_frame = tk.Frame(self.main_frame, bg="#0b0c3e")
        self.game_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.player_frame = tk.Frame(self.game_frame, bg="#0b0c3e")
        self.player_frame.grid(row=0, column=0, padx=10)

        self.ai_frame = tk.Frame(self.game_frame, bg="#0b0c3e")
        self.ai_frame.grid(row=0, column=1, padx=10)

        self.log_frame = tk.Frame(self.main_frame, bg="#0b0c3e")
        self.log_frame.pack(side="bottom", pady=10)

        # Set up team UI with buttons and progress bars
        self.setup_team_ui()

    def create_buttons(self):
        # Create Attack and Restart buttons once
        self.attack_button = tk.Button(self.main_frame, text="Perform Attack", command=self.perform_attack)
        self.attack_button.pack(pady=10)

        self.restart_button = tk.Button(self.main_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

    def draw_starry_sky(self):
        """Draw random stars on the canvas background."""
        for _ in range(200):  # Adjust the number of stars if needed
            x = random.randint(0, 800)  # Random x position
            y = random.randint(0, 600)  # Random y position
            self.canvas.create_oval(x, y, x + 2, y + 2, fill="white", outline="white")  # Small white dots as stars

    def setup_team_ui(self):
        """Set up player and AI team UI with buttons and progress bars."""
        self.player_buttons = []
        self.player_exp_bars = []
        for i in range(3):
            button = tk.Button(self.player_frame, text=f"Player {i + 1}", command=lambda i=i: self.choose_attacker(i), fg="green")
            button.pack(pady=5)
            self.player_buttons.append(button)
            exp_bar = ttk.Progressbar(self.player_frame, length=200, mode="determinate")
            exp_bar.pack(pady=5)
            self.player_exp_bars.append(exp_bar)

        self.ai_buttons = []
        self.ai_exp_bars = []
        for i in range(3):
            button = tk.Button(self.ai_frame, text=f"AI {i + 1}", command=lambda i=i: self.choose_target(i), fg="purple")
            button.pack(pady=5)
            self.ai_buttons.append(button)
            exp_bar = ttk.Progressbar(self.ai_frame, length=200, mode="determinate")
            exp_bar.pack(pady=5)
            self.ai_exp_bars.append(exp_bar)

        # Log display box in the log_frame
        self.log_display = tk.Text(self.log_frame, width=50, height=10, wrap="word", state="disabled")
        self.log_display.pack()

    def prompt_player_names(self):
        """Prompt each player for their character name."""
        for i in range(3):  # Assuming 3 players
            name = askstring("Player Name", f"Enter the name for Player {i + 1}:")
            if name:
                self.game.player_team[i].name = name
        # Refresh display to update button labels with new names
        self.refresh_display()

    def refresh_display(self):
        """Update the player and AI team buttons with HP and level details."""
        for idx, unit in enumerate(self.game.player_team):
            self.player_buttons[idx].config(text=f"{unit.name} (HP: {unit.hp}, Level: {unit.level})")
            exp_progress = (unit.exp / 100) * 100  # 100 represents EXP_THRESHOLD
            self.player_exp_bars[idx]['value'] = exp_progress

        for idx, unit in enumerate(self.game.ai_team):
            self.ai_buttons[idx].config(text=f"{unit.name} (HP: {unit.hp}, Level: {unit.level})")
            exp_progress = (unit.exp / 100) * 100  # 100 represents EXP_THRESHOLD
            self.ai_exp_bars[idx]['value'] = exp_progress

    def restart_game(self):
        """Restart the game and reset the GUI display."""
        self.game.restart_game()
        self.refresh_display()
        self.log_display.config(state="normal")
        self.log_display.delete(1.0, "end")
        self.log_display.config(state="disabled")
        self.log_message("The game has been restarted.")
        # Prompt for player names again on game restart
        self.prompt_player_names()

    def update_battle_log(self):
        # Add the event log to your battle log display here
        battle_log_text = "\n".join(self.game.event_log)  # Assuming event_log holds the game events
        self.log_display.config(state="normal")  # Assuming you're using a Text widget for battle log
        self.log_display.delete(1.0, "end")
        self.log_display.insert("end", battle_log_text)
        self.log_display.config(state="disabled")

    def perform_attack(self):
        if self.attacker_index is None or self.target_index is None:
            return

        # Get the attacker and target based on the selected indexes
        player_unit = self.game.player_team[self.attacker_index]
        target_unit = self.game.ai_team[self.target_index]

        # Player attacks
        damage, exp_earned = player_unit.attack(target_unit)
        self.game.record_event(f"{player_unit.name} attacked {target_unit.name} and inflicted {damage} damage.")

        # Check if the AI team is still alive after the attack
        if self.game.check_game_over():
            self.display_winner("Player Team")
            return

        # AI attacks back
        self.game.ai_turn()  # AI retaliates by attacking

        # Check if the player team is still alive after the AI's counterattack
        if self.game.check_game_over():
            self.display_winner("AI Team")
            return

        # Update the battle log and refresh the UI after the attack
        self.update_battle_log()
        self.refresh_display()

    def choose_attacker(self, index):
        self.attacker_index = index
        self.log_message(f"Attacker selected: {self.game.player_team[index].name}")

    def choose_target(self, index):
        self.target_index = index
        self.log_message(f"Target selected: {self.game.ai_team[index].name}")

    def log_message(self, message):
        self.log_display.config(state="normal")
        self.log_display.insert("end", f"{message}\n")
        self.log_display.config(state="disabled")

    def display_winner(self, winning_team):
        messagebox.showinfo("Game Over", f"{winning_team} wins!")
        self.restart_game()


if __name__ == "__main__":
    # Build teams for the game
    player_team = build_team("Player")
    ai_team = build_team("AI")

    # Create the Game instance
    game_instance = Game(player_team, ai_team)

    # Create the main tkinter window
    root = tk.Tk()

    # Create the GameGUI instance
    gui = GameGUI(root, game_instance)

    # Start the tkinter main loop
    root.mainloop()