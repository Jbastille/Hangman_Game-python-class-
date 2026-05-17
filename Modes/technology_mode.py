from Game.game_mode import GameMode


class TechnologyMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Technology"

        self.background_image = "assets/background_images/Technology.png"

        self.background_color = "#e6e6e6"

        self.word_folder = "technology"