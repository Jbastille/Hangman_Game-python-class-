import json
import os
from settings.Themes import THEMES


class SettingsManager:
    def __init__(self):
        # Path to config.json inside the settings folder
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")

        # Load settings from JSON
        self.load()

    # ---------------------------------------------------------
    # LOAD SETTINGS
    # ---------------------------------------------------------
    def load(self):
        with open(self.config_path, "r") as f:
            self.data = json.load(f)

        # Extract values from JSON
        self.theme_name = self.data["theme"]
        self.music_volume = self.data["music_volume"]
        self.sfx_volume = self.data["sfx_volume"]
        self.screen_size = self.data["screen_size"]
        self.fullscreen = self.data["fullscreen"]

        # Load theme colors from themes.py
        self.Theme = themes[self.theme_name]

    # ---------------------------------------------------------
    # SAVE SETTINGS
    # ---------------------------------------------------------
    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.data, f, indent=4)

    # ---------------------------------------------------------
    # THEME FUNCTIONS
    # ---------------------------------------------------------
    def apply_theme(self, theme_name):
        self.theme_name = theme_name
        self.data["theme"] = theme_name
        self.theme = themes[theme_name]

    def apply_theme_to_window(self, window):
        window.configure(bg=self.theme["bg"])

    # ---------------------------------------------------------
    # VOLUME FUNCTIONS
    # ---------------------------------------------------------
    def set_music_volume(self, value):
        self.music_volume = int(value)
        self.data["music_volume"] = self.music_volume

    def set_sfx_volume(self, value):
        self.sfx_volume = int(value)
        self.data["sfx_volume"] = self.sfx_volume

    # ---------------------------------------------------------
    # DISPLAY FUNCTIONS
    # ---------------------------------------------------------
    def set_screen_size(self, size):
        self.screen_size = size
        self.data["screen_size"] = size

    def apply_window_size(self, window):
        window.geometry(self.screen_size)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.data["fullscreen"] = self.fullscreen

    # ---------------------------------------------------------
    # RESET TO DEFAULTS
    # ---------------------------------------------------------
    def reset(self):
        # Reset to default values
        self.data = {
            "theme": "dark",
            "music_volume": 70,
            "sfx_volume": 70,
            "screen_size": "1280x720",
            "fullscreen": False
        }
        self.save()
        self.load()
