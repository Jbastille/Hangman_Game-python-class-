import tkinter as tk


class DifficultyFrame(tk.Frame):

    def __init__(self, master, settings, mode):

        super().__init__(master)

        self.master = master
        self.settings = settings
        self.mode = mode

        bg = settings.theme["bg"]
        fg = settings.theme["fg"]

        self.config(bg=bg)

        title = tk.Label(
            self,
            text=f"{mode.name} Difficulty",
            font=("Arial", 28, "bold"),
            bg=bg,
            fg=fg
        )

        title.pack(pady=30)

        difficulties = [
            "easy",
            "medium",
            "hard"
        ]

        for difficulty in difficulties:

            tk.Button(
                self,
                text=difficulty.capitalize(),
                font=("Arial", 18),
                width=20,
                height=2,
                command=lambda d=difficulty:
                    self.start_game(d)
            ).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            font=("Arial", 14),
            width=15,
            command=self.master.show_categories
        ).pack(pady=25)

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------
    def start_game(self, difficulty):

        self.mode.load_words(difficulty)

        self.master.start_game(
            self.mode,
            difficulty
        )