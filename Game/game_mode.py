import random


class GameMode:

    def __init__(self):

        self.name = "Default"

        self.background_color = "#ffffff"

        self.background_image = None

        self.words = []

    def get_random_word(self):

        return random.choice(self.words)