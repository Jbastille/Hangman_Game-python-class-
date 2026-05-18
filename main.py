#!/usr/bin/env python3
"""
i added  Geuset or  login page 

"""

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

from gui.main_window import MainWindow
from gui.sound_manager import SoundManager


class Launcher:
    def __init__(self):
        self.root = tk.Tk() # main container
        self.root.title("Hangman Game")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Load background image from media 
        self.bg_image = None    # to avoid deleting the link by garbage collector
        self.bg_label = None
        self.setup_background()

        # Center the window on screen
        self.center_window()

        self.user_id = None     #place holder
        self.username = None

        self.create_widgets()

    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_background(self):
        """ assets/media/login_bg.jpg """
        bg_path = "assets/media/login_bg.jpg"
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path)
                img = img.resize((1000, 700), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.bg_label = tk.Label(self.root, image=self.bg_image)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Could not load background: {e}")
                self.root.configure(bg="#1a1a2e")
        else:
            # No background found, use solid color
            self.root.configure(bg="#1a1a2e")

    def create_widgets(self):
        """Create UI elements above the background."""
        # Use  overlay frame for better text readability
        overlay = tk.Frame(self.root, bg="#0f0f1a", bd=0)
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Title
        title_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
        title = tk.Label(
            overlay,
            text="HANGMAN",
            font=title_font,
            fg="#FFD700",
            bg="#0f0f1a"
        )
        title.pack(pady=(40, 10))

        subtitle = tk.Label(
            overlay,
            text="The Classic Word Guessing Game",
            font=("Helvetica", 14),
            fg="#cccccc",
            bg="#0f0f1a"
        )
        subtitle.pack(pady=(0, 30))

        # Button styling
        button_font = ("Helvetica", 14, "bold")
        button_bg = "#2c2c3e"
        button_fg = "#ffffff"
        button_active_bg = "#4a4a6a"

        # Play as Guest button
        guest_btn = tk.Button(
            overlay,
            text=" Play as Guest",
            font=button_font,
            bg=button_bg,
            fg=button_fg,
            activebackground=button_active_bg,
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.play_as_guest
        )
        guest_btn.pack(pady=15)

        # Login / Sign Up button
        login_btn = tk.Button(
            overlay,
            text=" Login / Sign Up",
            font=button_font,
            bg=button_bg,
            fg=button_fg,
            activebackground=button_active_bg,
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.open_login
        )
        login_btn.pack(pady=15)

        # Quit button
        quit_btn = tk.Button(
            overlay,
            text=" Quit",
            font=("Helvetica", 12),
            bg="#1f1f2e",
            fg="#ff8888",
            activebackground="#3a1a1a",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=5,
            command=self.root.quit
        )
        quit_btn.pack(pady=(30, 20))

        # Optional: credit line
        credit = tk.Label(
            overlay,
            text="© Hangman Game - Your Name",
            font=("Helvetica", 8),
            fg="#666666",
            bg="#0f0f1a"
        )
        credit.pack(side="bottom", pady=10)

    def play_as_guest(self):
        """Guest mode: no database, no saving."""
        SoundManager.play("click")
        self.user_id = None
        self.username = "Guest"
        self.start_game()

    def open_login(self):
        """Open login/signup window."""
        SoundManager.play("click")
        from gui.login_window import LoginWindow
        LoginWindow(self.root, on_login_success=self.on_login_ok)

    def on_login_ok(self, user_id, username):
        """Called after successful login/signup."""
        self.user_id = user_id
        self.username = username
        self.start_game()

    def start_game(self):
        """Destroy launcher and start the main game window."""
        self.root.destroy()
        app = MainWindow(user_id=self.user_id, username=self.username)
        app.mainloop()


if __name__ == "__main__":
    launcher = Launcher()
    launcher.root.mainloop()