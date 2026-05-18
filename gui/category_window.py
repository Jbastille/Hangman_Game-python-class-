import tkinter as tk

from Modes.animals_mode import AnimalsMode
from Modes.food_mode import FoodMode
from Modes.countries_mode import CountriesMode
from Modes.sports_mode import SportsMode
from Modes.technology_mode import TechnologyMode


class CategoryFrame(tk.Frame):

    def __init__(self, master, settings):
        super().__init__(master)

        self.master = master
        self.settings = settings

        bg = settings.theme["bg"]
        fg = settings.theme["fg"]

        self.config(bg=bg)

        title = tk.Label(
            self,
            text="Choose Category",
            font=("Freestyle script", 28, "bold"),
            bg=bg,
            fg=fg
        )
        title.pack(pady=30)

        modes = [
            AnimalsMode(),
            FoodMode(),
            CountriesMode(),
            SportsMode(),
            TechnologyMode()
        ]

        for mode in modes:
            tk.Button(
                self,
                text=mode.name,
                font=("Freestyle script", 16),
                width=20,
                height=2,
                command=lambda m=mode:
                    self.master.show_difficulties(m)
            ).pack(pady=8)

       
        tk.Button(
            self,
            text="Back",
            font=("Arial", 14),
            width=15,
            command=self.master.show_main_menu
        ).pack(pady=25)