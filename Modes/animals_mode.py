from Game.game_mode import GameMode
import pygame

class AnimalsMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Animals"

        self.background_color = "#dff6dd"

        self.background_image = "assets/background_images/Animals.png"




        self.words = [
            ("elephant", "Largest land animal"),
            ("penguin", "Flightless bird"),
            ("giraffe", "Tall African animal")
        ]