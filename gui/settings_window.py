import tkinter as tk
from tkinter import ttk
from settings.Themes import THEMES
#______--------____________----------------__________--__________-------------_____________-------------_________
# using OOP principals and guides from Documentation and Copilot. I will create classes and funtions 
# that call upon a master injection parameter that allows this to be stored from a database if it stored that way
# This will allow us to use JSON files for storing data and inject it into out program.
#___________------------____________--------------________--------------____________-------------------______-----

class SettingsWindow(tk.Toplevel):

    def __init__(self, master, settings_manager):
        super().__init__(master)
        self.settings = settings_manager

        self.title("Settings")
        self.geometry("400x400")
        self.configure(bg="#2b2b2b")

        self.create_layout()

    # ---------------------------------------------------------
    # LAYOUT
    # ---------------------------------------------------------
    def create_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, width=150, bg="#1e1e1e")
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.content = tk.Frame(self, bg="#2b2b2b")
        self.content.pack(side="right", expand=True, fill="both")

        # Sidebar buttons
        buttons = [
            ("Audio", self.show_audio_settings),
            ("Theme", self.show_theme_settings),
            ("Display", self.show_display_settings),
            ("Save", self.show_save_settings)
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#333333",
                fg="white",
                relief="flat",
                height=2
            )
            btn.pack(fill="x", pady=2)

        # Default panel
        self.show_audio_settings()

    # Clears the content panel
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # AUDIO SETTINGS
    # ---------------------------------------------------------
    def show_audio_settings(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Audio Settings",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 16)
        ).pack(pady=10)

        tk.Label(self.content, text="Music Volume", fg="white", bg="#2b2b2b").pack()
        tk.Scale(
            self.content,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.settings.set_music_volume
        ).pack()

        tk.Label(self.content, text="SFX Volume", fg="white", bg="#2b2b2b").pack()
        tk.Scale(
            self.content,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.settings.set_sfx_volume
        ).pack()

    # ---------------------------------------------------------
    # THEME SETTINGS
    # ---------------------------------------------------------
    def show_theme_settings(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Theme Settings",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 16)
        ).pack(pady=10)

        # StringVar to track selected theme
        self.theme_var = tk.StringVar(value=self.settings.theme_name)

        tk.Radiobutton(
            self.content,
            text="Light Theme",
            variable=self.theme_var,
            value="light",
            command=self.change_theme,
            bg="#2b2b2b",
            fg="white",
            selectcolor="#444"
        ).pack(anchor="w")

        tk.Radiobutton(
            self.content,
            text="Dark Theme",
            variable=self.theme_var,
            value="dark",
            command=self.change_theme,
            bg="#2b2b2b",
            fg="white",
            selectcolor="#444"
        ).pack(anchor="w")

    def change_theme(self):
        new_theme = self.theme_var.get()

        # Update settings object
        self.settings.theme_name = new_theme
        self.settings.theme = THEMES[new_theme]

        # Save to config.json
        self.settings.save()

        # Apply theme to this window
        self.settings.apply_theme_to_window(self)

        # Recolor widgets inside settings window
        for widget in self.winfo_children():
            try:
                widget.configure(
                    bg=self.settings.theme["bg"],
                    fg=self.settings.theme["fg"]
                )
            except:
                pass

        # Apply theme to main window
        self.settings.apply_theme_to_window(self.master)

    # ---------------------------------------------------------
    # DISPLAY SETTINGS
    # ---------------------------------------------------------
    def show_display_settings(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Display Settings",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 16)
        ).pack(pady=10)

        tk.Label(self.content, text="Screen Size", fg="white", bg="#2b2b2b").pack()

        sizes = ["800x600", "1280x720", "1920x1080"]
        size_var = tk.StringVar(value=self.settings.screen_size)

        tk.OptionMenu(
            self.content,
            size_var,
            *sizes,
            command=self.settings.set_screen_size
        ).pack()

        tk.Checkbutton(
            self.content,
            text="Fullscreen",
            command=self.settings.toggle_fullscreen,
            bg="#2b2b2b",
            fg="white",
            selectcolor="#444"
        ).pack()

    # ---------------------------------------------------------
    # SAVE SETTINGS
    # ---------------------------------------------------------
    def show_save_settings(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Save Settings",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 16)
        ).pack(pady=10)

        tk.Button(
            self.content,
            text="Save",
            command=self.settings.save,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            self.content,
            text="Reset to Default",
            command=self.settings.reset,
            bg="#E53935",
            fg="white"
        ).pack(pady=10)
