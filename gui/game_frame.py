import tkinter as tk
import random
from PIL import Image, ImageTk
import pygame

from assets.sounds.audio_manager import AudioManager

class GameFrame(tk.Frame):
    def __init__(self, master, settings, game_mode):
        super().__init__(master)

        self.master = master

        self.pack(fill="both", expand=True)

        self.game_mode = game_mode
        self.setup_background()
        self.settings = settings
        self.settings.apply_theme_to_window(self)

        # Word list (you can replace this with a file later) #done
        word_data = self.game_mode.get_random_word()

        # Game state
        self.secret_word = word_data[0]
        self.hint = word_data[1]
        self.guessed_letters = set()
        self.lives = 6

        # Build UI
        self.create_layout()
        self.update_word_display()
        self.update_hangman_display()
        
        #creating the sounds
        pygame.mixer.init()
        self.win_sound = pygame.mixer.Sound("assets/sounds/chime_up.wav")
        self.lose_sound = pygame.mixer.Sound("assets/sounds/whah_whah.wav")
        self.click_sound = pygame.mixer.Sound("assets/sounds/floop2_x.wav")

      


    #SOUND EFFECTS FUNCTION
    def play_click_sound(self, letter):
        self.click_sound.play()
        self.guess_letter(letter.lower())

    # ---------------------------------------------------------
    # UI LAYOUT
    # ---------------------------------------------------------
    def create_layout(self):
        theme = self.settings.theme

        self.category_label = tk.Label(
            self,
            text=self.game_mode.name,
            font=("Arial", 20, "bold"),
            bg=self.game_mode.background_color
        )
        self.category_label.pack(pady=10)

        self.hint_label = tk.Label(
            self,
            text=f"Hint: {self.hint}",
            font=("Arial", 14),
            bg=self.game_mode.background_color
        )
        self.hint_label.pack()


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
            command=self.master.show_categories
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

        word_data = self.game_mode.get_random_word()

        self.secret_word = word_data[0]
        self.hint = word_data[1]

        self.guessed_letters = set()
        self.lives = 6

        self.hint_label.config(
        text=f"Hint: {self.hint}"
        )

        self.lives_label.config(
        text=f"Lives: {self.lives}"
        )

        self.update_word_display()
        self.update_hangman_display()

        for widget in self.buttons_frame.winfo_children():
            widget.config(state="normal")


    def setup_background(self):

        # Load image
        image = Image.open(
            self.game_mode.background_image
        )

        # Resize image to window size
        image = image.resize((1280, 720))

        self.bg_image = ImageTk.PhotoImage(image)

        # Background label
        self.bg_label = tk.Label(
            self,
            image=self.bg_image
        )

        self.bg_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )