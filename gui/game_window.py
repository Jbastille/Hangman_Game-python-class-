import tkinter as tk
import random


class GameWindow(tk.Toplevel):
    def __init__(self, master, settings):
        super().__init__(master)

        self.settings = settings
        self.title("Hangman")
        self.settings.apply_theme_to_window(self)
        self.settings.apply_window_size(self)

        # Word list (you can replace this with a file later)
        self.words = ["python", "hangman", "developer", "project", "settings"]

        # Game state
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.lives = 6

        # Build UI
        self.create_layout()
        self.update_word_display()
        self.update_hangman_display()

    # ---------------------------------------------------------
    # UI LAYOUT
    # ---------------------------------------------------------
    def create_layout(self):
        theme = self.settings.theme

        # Word display
        self.word_label = tk.Label(
            self,
            text="",
            font=("Arial", 32),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        self.word_label.pack(pady=20)

        # Hangman drawing
        self.hangman_label = tk.Label(
            self,
            text="",
            font=("Courier", 20),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        self.hangman_label.pack(pady=10)

        # Lives counter
        self.lives_label = tk.Label(
            self,
            text=f"Lives: {self.lives}",
            font=("Arial", 16),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        self.lives_label.pack(pady=10)

        # Alphabet buttons
        self.buttons_frame = tk.Frame(self, bg=theme["bg"])
        self.buttons_frame.pack(pady=20)

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            btn = tk.Button(
                self.buttons_frame,
                text=letter,
                width=4,
                command=lambda l=letter: self.guess_letter(l.lower())
            )
            btn.pack(side="left", padx=2, pady=2)

        # Bottom buttons
        bottom = tk.Frame(self, bg=theme["bg"])
        bottom.pack(pady=20)

        tk.Button(
            bottom,
            text="Restart",
            command=self.restart_game
        ).pack(side="left", padx=10)

        tk.Button(
            bottom,
            text="Back to Menu",
            command=self.destroy
        ).pack(side="left", padx=10)

    # ---------------------------------------------------------
    # GAME LOGIC
    # ---------------------------------------------------------
    def update_word_display(self):
        display = " ".join(
            [letter if letter in self.guessed_letters else "_" for letter in self.secret_word]
        )
        self.word_label.config(text=display)

    def update_hangman_display(self):
        stages = [
            "",
            "O",
            "O\n |",
            "O\n/|",
            "O\n/|\\",
            "O\n/|\\\n/",
            "O\n/|\\\n/ \\"
        ]
        self.hangman_label.config(text=stages[6 - self.lives])

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)

        if letter not in self.secret_word:
            self.lives -= 1
            self.lives_label.config(text=f"Lives: {self.lives}")
            self.update_hangman_display()

            if self.lives == 0:
                self.word_label.config(text=f"You lost! Word was: {self.secret_word}")
                self.disable_buttons()
                return

        self.update_word_display()

        if all(l in self.guessed_letters for l in self.secret_word):
            self.word_label.config(text="You won!")
            self.disable_buttons()

    def disable_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.config(state="disabled")

    def restart_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.lives = 6

        self.lives_label.config(text=f"Lives: {self.lives}")
        self.update_word_display()
        self.update_hangman_display()

        for widget in self.buttons_frame.winfo_children():
            widget.config(state="normal")
