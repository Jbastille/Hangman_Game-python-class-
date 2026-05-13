import tkinter as tk
from tkinter import ttk

from settings.settings_manager import SettingsManager
from gui.settings_window import settingsWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load settings
        self.settings = SettingsManager()

        # Apply theme + window size
        self.settings.apply_theme_to_window(self)
        self.settings.apply_window_size(self)

        # Window title
        self.title("Hangman Game")

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title = tk.Label(
            self,
            text="Hangman Game",
            font=("Arial", 32),
            bg=self.settings.theme["bg"],
            fg=self.settings.theme["fg"]
        )
        title.pack(pady=40)

        # Start Game button
        start_btn = tk.Button(
            self,
            text="Start Game",
            font=("Arial", 18),
            width=20,
            command=self.start_game
        )
        start_btn.pack(pady=10)

        # Settings button
        settings_btn = tk.Button(
            self,
            text="Settings",
            font=("Arial", 18),
            width=20,
            command=self.open_settings
        )
        settings_btn.pack(pady=10)

        # Quit button
        quit_btn = tk.Button(
            self,
            text="Quit",
            font=("Arial", 18),
            width=20,
            command=self.quit
        )
        quit_btn.pack(pady=10)

    def open_settings(self):
        settingsWindow(self, self.settings)

    def start_game(self):
        print("Game will start here later!")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

