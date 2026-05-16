import tkinter as tk
import random
import pygame


class GameWindow(tk.Toplevel):
    def __init__(self, master, settings):
        super().__init__(master)

        self.settings = settings
        self.title("Hangman")
        self.settings.apply_theme_to_window(self)
        self.settings.apply_window_size(self)

        # This will initilize the music / sounds effects
        pygame.mixer.init()
        self.play_background_music()
        
        self.win_sound = pygame.mixer.Sound("assets/sounds/chime_up.wav")
        self.lose_sound = pygame.mixer.Sound("assets/sounds/whah_whah.wav")
        self.click_sound = pygame.mixer.Sound("assets/sounds/floop2_x.wav")

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


    # MUSIC Function 
    def play_background_music(self):
            try:
                pygame.mixer.music.load("assets/sounds/after-dark-reflections.mp3")
                pygame.mixer.music.set_volume(self.settings.music_volume / 100)
                pygame.mixer.music.play(-1) 
            except Exception as ex:
                print("Error loading music:", ex)

    def destroy(self):
        pygame.mixer.music.stop()
        super().destroy()

    #SOUND EFFECTS FUNCTION
    def play_click_sound(self, letter):
        self.click_sound.play()
        self.guess_letter(letter.lower())
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
                command=lambda l=letter: self.play_click_sound(l)

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
                self.lose_sound.play()
                self.word_label.config(text=f"You lost! Word was: {self.secret_word}")
                self.disable_buttons()
                return


        self.update_word_display()

        if all(l in self.guessed_letters for l in self.secret_word):
            self.win_sound.play()
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
