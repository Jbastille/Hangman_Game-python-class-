import pygame
import os

class SoundManager:
    _initialized = False

    @classmethod
    def _init_mixer(cls):
        if not cls._initialized:
            pygame.mixer.init()
            cls._initialized = True

    @classmethod
    def play(cls, sound_name):
        """sound_name: e.g. 'click', 'success', 'error', 'pop'"""
        cls._init_mixer()
        file_path = os.path.join("assets", "media", f"{sound_name}.mp3")
        if os.path.exists(file_path):
            try:
                pygame.mixer.Sound(file_path).play()
            except:
                pass  # fail silently