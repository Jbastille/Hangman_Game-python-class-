import tkinter as tk
import random
from PIL import Image, ImageTk
import pygame

from assets.sounds.audio_manager import AudioManager

class GameFrame(tk.Frame):
    def __init__(self, master, settings, game_mode, difficulty):
        super().__init__(master)

        self.master = master

        self.pack(fill="both", expand=True)

        self.game_mode = game_mode
        self.difficulty = difficulty
        self.setup_background()
        self.settings = settings
        self.settings.apply_theme_to_window(self)

        # Word list (you can replace this with a file later) #done
        reveal_limits = {
            "easy": float("inf"),
            "medium": 2,
            "hard": 1
        }

        self.remaining_reveals = reveal_limits[difficulty]

        difficulty_lives = {
            "easy": 6,
            "medium": 5,
            "hard": 4
        }

        self.lives = difficulty_lives[difficulty]

        difficulty_times = {
            "easy": 120,
            "medium": 90,
            "hard": 60
        }

        self.time_left = difficulty_times[difficulty]


        #this is where you can put the word list
        word_data = self.game_mode.get_random_word()

       
        self.secret_word = word_data[0]
        self.hint = word_data[1]
        self.guessed_letters = set()

        # Building the UserIterface
        self.create_layout()
        self.update_word_display()
        self.update_hangman_display()
        
 
        pygame.mixer.init()
        self.win_sound = pygame.mixer.Sound("assets/sounds/chime_up.wav")
        self.lose_sound = pygame.mixer.Sound("assets/sounds/whah_whah.wav")
        self.click_sound = pygame.mixer.Sound("assets/sounds/floop2_x.wav")

      


    #SOUND EFFECTS FUNCTION
    def play_click_sound(self, letter):
        self.click_sound.play()
        self.guess_letter(letter.lower())
        self.timer_running = True
        self.update_timer()

    def create_layout(self):
        theme = self.settings.theme

        self.category_label = tk.Label(
            self,
            text=self.game_mode.name,
            font=("Arial", 20, "bold"),
            bg=self.game_mode.background_color
        )
        self.category_label.pack(pady=10)


        self.difficulty_label = tk.Label(
            self,
            text=f"Difficulty: {self.difficulty.capitalize()}",
            font=("Arial", 14),
            bg="#222222",
            fg="white"
        )

        self.difficulty_label.pack()


        self.hint_label = tk.Label(
            self,
            text=f"Hint: {self.hint}",
            font=("Arial", 14),
            bg=self.game_mode.background_color
        )
        self.hint_label.pack()

        self.timer_label = tk.Label(
            self,
            text=f"Time Left: {self.time_left}",
            font=("Arial", 14),
            bg="#222222",
            fg="white"
        )

        self.timer_label.pack()

        if self.remaining_reveals == float("inf"):
            reveal_text = "Reveals: Unlimited"
        else:
            reveal_text = f"Reveals Left: {self.remaining_reveals}"

        self.reveal_label = tk.Label(
            self,
            text=reveal_text,
            font=("Arial", 14),
            bg="#222222",
            fg="white"
        )

        self.reveal_label.pack()

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
        text="Reveal Letter",
        command=self.reveal_letter
        ).pack(side="left", padx=10)

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
                self.timer_running = False
                self.disable_buttons()
                return

        self.update_word_display()

        if all(l in self.guessed_letters for l in self.secret_word):
            self.win_sound.play()
            self.word_label.config(text="You won!")
            self.timer_running = False
            self.disable_buttons()

    def disable_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.config(state="disabled")

    def restart_game(self):

        word_data = self.game_mode.get_random_word()

        self.secret_word = word_data[0]
        self.hint = word_data[1]

        self.guessed_letters = set()
        difficulty_lives = {
            "easy": 6,
            "medium": 5,
            "hard": 4
        }

        self.lives = difficulty_lives[self.difficulty]

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

        if hasattr(self, "timer_id"):
            self.after_cancel(self.timer_id)

        difficulty_times = {
            "easy": 120,
            "medium": 90,
            "hard": 60
        }

        self.time_left = difficulty_times[self.difficulty]

        self.timer_running = True
        self.update_timer()



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

    def update_timer(self):

        if not self.timer_running:
            return

        minutes = self.time_left // 60
        seconds = self.time_left % 60

        self.timer_label.config(
            text=f"Time Left: {minutes:02}:{seconds:02}"
        )

        if self.time_left > 0:

            self.time_left -= 1

            self.timer_id = self.after(
                1000,
                self.update_timer
            )

        else:

            self.timer_running = False

            self.word_label.config(
            text=f"Time's up! Word was: {self.secret_word}"
            )

            self.disable_buttons()

    def reveal_letter(self):

        # No reveals left
        if self.remaining_reveals <= 0:
            return

        # Find hidden letters
        hidden_letters = [
            letter for letter in self.secret_word
            if letter not in self.guessed_letters
        ]

        # Word already solved
        if not hidden_letters:
            return

        # Choose random hidden letter
        revealed_letter = random.choice(hidden_letters)

        # Add to guessed letters
        self.guessed_letters.add(revealed_letter)

        # Reduce reveals if not unlimited
        if self.remaining_reveals != float("inf"):
            self.remaining_reveals -= 1

        # Update reveal label
        if self.remaining_reveals == float("inf"):
            text = "Reveals: Unlimited"
        else:
            text = f"Reveals Left: {self.remaining_reveals}"

        self.reveal_label.config(text=text)

        # Update word display
        self.update_word_display()

        # Check win
        if all(l in self.guessed_letters for l in self.secret_word):

            self.word_label.config(text="You won!")

            self.timer_running = False

            self.disable_buttons()