import tkinter as tk

from gui.settings_window import SettingsWindow


class MainMenuFrame(tk.Frame):

    def __init__(self, master, settings):

        super().__init__(master)

        self.master = master
        self.settings = settings

        bg = settings.theme["bg"]
        fg = settings.theme["fg"]

        self.config(bg=bg)

        title = tk.Label(
            self,
            text="Hangman Game",
            font=("Freestyle script", 60, "bold"),
            bg=bg,
            fg=fg
        )

        title.pack(pady=40)

        # Start button
        tk.Button(
            self,
            text="Start Game",
            font=("Freestyle script", 18),
            width=20,
            command=self.master.show_categories
        ).pack(pady=10)

        # Settings
        tk.Button(
            self,
            text="Settings",
            font=("Freestyle script", 18),
            width=20,
            command=self.open_settings
        ).pack(pady=10)

        # Quit
        tk.Button(
            self,
            text="Quit",
            font=("Freestyle script", 18),
            width=20,
            command=self.master.quit
        ).pack(pady=10)

    def open_settings(self):

        SettingsWindow(
            self.master,
            self.settings
        )