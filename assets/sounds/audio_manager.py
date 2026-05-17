import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.7

    def play_music(self, file, loop=True):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if loop else 0)

    def play_sfx(self, file):
        sound = pygame.mixer.Sound(file)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()


    CATEGORY_MUSIC = {
    "Animals": "assets/sounds/acoustic-countryside-journey.mp3",
    "Food": "assets/sounds/Pufino - Serenity (freetouse.com).mp3",
    "Countries": "assets/sounds/Filo Starquez - Park Vibes (freetouse.com).mp3",
    "Sports": "assets/sounds/Aylex - Snap Attack (freetouse.com).mp3",
    "Technology": "assets/sounds/Walen - Gameboy (freetouse.com)mp3"
}
