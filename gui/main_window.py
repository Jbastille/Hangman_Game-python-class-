import tkinter as tk

from settings.settings_manager import SettingsManager
from assets.sounds.audio_manager import AudioManager

from assets.sounds.Theme_Music import CATEGORY_MUSIC

from gui.main_menu_frame import MainMenuFrame
from gui.category_frame import CategoryFrame
from gui.game_frame import GameFrame
from gui.difficulty_frame import DifficultyFrame


class MainWindow(tk.Tk):

    def __init__(self, user_id=None, username="Guest"):

        super().__init__()

        self.user_id = user_id
        self.username = username

        self.audio = AudioManager()

        self.settings = SettingsManager()

        self.title("Hangman")

        self.settings.apply_theme_to_window(self)
        self.settings.apply_window_size(self)

        self.current_frame = None

        self.show_main_menu()

    # ---------------------------------------------------------
    # FRAME SWITCHING
    # ---------------------------------------------------------
    def switch_frame(self, new_frame):

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # SCREENS
    # ---------------------------------------------------------
    def show_main_menu(self):

        frame = MainMenuFrame(self, self.settings)

        self.switch_frame(frame)

    def show_categories(self):

        frame = CategoryFrame(self, self.settings)

        self.switch_frame(frame)

    def show_difficulties(self, mode):

        # Play category background music
        music_file = CATEGORY_MUSIC.get(mode.name)
        if music_file:
            self.audio.play_music(music_file)

        # Show difficulty selection screen
        frame = DifficultyFrame(
            self,
            self.settings,
            mode
        )

        self.switch_frame(frame)


    # I pass user_id (if None, use self.user_id in geust case)
    def start_game(self, mode, difficulty, user_id=None):
        
        if user_id is None:
            user_id = self.user_id
        frame = GameFrame(self, self.settings, mode, difficulty, user_id=user_id)

        self.switch_frame(frame)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":

    app = MainWindow()
    app.mainloop()