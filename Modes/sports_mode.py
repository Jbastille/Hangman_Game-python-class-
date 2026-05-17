from Game.game_mode import GameMode


class SportsMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Sports"

        self.background_image = "assets/background_images/Sports.png"

        self.background_color = "#f5d9ff"

        self.word_folder = "sports"