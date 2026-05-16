import tkinter as tk
from tkinter import ttk
from settings.settings_manager import SettingsManager
from gui.settings_window import SettingsWindow
from gui.game_window import GameWindow



class MainWindow(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.root.title("Hangman")

        # Load settings
        self.settings = SettingsManager()

        # Apply theme and window size to game window
        self.settings.apply_theme_to_window(self.root)
        self.settings.apply_window_size(self.root)
        self.configure(bg=self.settings.theme["bg"])

        self.pack(fill="both", expand=True)


        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title = tk.Label(
            self,
            text="Hangman Game",
            font=("Freestyle script", 60),
            bg=self.settings.theme["bg"],
            fg=self.settings.theme["fg"]
        )
        title.pack(pady=40)

        # Start Game button
        start_btn = tk.Button(
            self,
            text="Start Game",
            font=("Freestyle script", 18),
            width=20,
            command=self.start_game
        )
        start_btn.pack(pady=10)

        # Settings button
        settings_btn = tk.Button(
            self,
            text="Settings",
            font=("Freestyle script", 18),
            width=20,
            command=self.open_settings
        )
        settings_btn.pack(pady=10)

        # Quit button
        quit_btn = tk.Button(
            self,
            text="Quit",
            font=("Freestyle script", 18),
            width=20,
            command=self.quit
        )
        quit_btn.pack(pady=10)

    def open_settings(self):
        SettingsWindow(self, self.settings)

    def start_game(self):
        GameWindow(self, self.settings)
    




if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

