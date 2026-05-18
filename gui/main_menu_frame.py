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

        #leaderboard
        tk.Button(
            self,
            text="Leaderboard",
            font=("Freestyle script", 18),
            width=20,
            command=self.open_leaderboard
        ).pack(pady=10)

        #profile 
        if self.master.user_id is not None:
            tk.Button(
                self,
                text="My Profile",
                font=("Freestyle script", 18),
                width=20,
                command=self.open_profile
            ).pack(pady=10)

    def open_profile(self):
        from gui.profile_window import ProfileWindow
        ProfileWindow(self.master, self.master.user_id, self.master.username)
    

    def open_leaderboard(self):
        from gui.leaderboard_window import LeaderboardWindow
        LeaderboardWindow(self.master)

    def open_settings(self):

        SettingsWindow(
            self.master,
            self.settings
        )