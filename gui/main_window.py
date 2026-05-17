import tkinter as tk

from settings.settings_manager import SettingsManager

from assets.sounds.audio_manager import AudioManager, CATEGORY_MUSIC

from gui.main_menu_frame import MainMenuFrame
from gui.category_frame import CategoryFrame
from gui.game_frame import GameFrame


class MainWindow(tk.Tk):

    def __init__(self):

        super().__init__()

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

    def start_game(self, mode):

    # Play category background music
     music_file = CATEGORY_MUSIC.get(mode.name)
     if music_file:
        self.audio.play_music(music_file)

     frame = GameFrame(
        self,
        self.settings,
        mode
    )

     self.switch_frame(frame)



# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":

    app = MainWindow()
    app.mainloop()