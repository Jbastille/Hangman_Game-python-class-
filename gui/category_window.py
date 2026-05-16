import tkinter as tk

from gui.game_window import GameWindow

from Modes.animals_mode import AnimalsMode
from Modes.food_mode import FoodMode
from Modes.countries_mode import CountriesMode
from Modes.sports_mode import SportsMode
from Modes.technology_mode import TechnologyMode


class CategoryWindow(tk.Toplevel):

    def __init__(self, master, settings):

        super().__init__(master)

        self.settings = settings

        self.title("Choose Category")

        self.settings.apply_theme_to_window(self)
        self.settings.apply_window_size(self)

        self.modes = [
            AnimalsMode(),
            FoodMode(),
            CountriesMode(),
            SportsMode(),
            TechnologyMode()
        ]

        self.create_widgets()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def create_widgets(self):

        bg = self.settings.theme["bg"]
        fg = self.settings.theme["fg"]

        title = tk.Label(
            self,
            text="Choose Category",
            font=("Arial", 28, "bold"),
            bg=bg,
            fg=fg
        )

        title.pack(pady=30)

        # Category buttons
        for mode in self.modes:

            btn = tk.Button(
                self,
                text=mode.name,
                font=("Arial", 16),
                width=20,
                height=2,
                command=lambda m=mode: self.start_game(m)
            )

            btn.pack(pady=8)

        # Back button
        back_btn = tk.Button(
            self,
            text="Back",
            font=("Arial", 14),
            width=15,
            command=self.destroy
        )

        back_btn.pack(pady=25)

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------
    def start_game(self, mode):

        GameWindow(
            self,
            self.settings,
            mode
        )