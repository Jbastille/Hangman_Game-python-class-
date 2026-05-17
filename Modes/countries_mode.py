from Game.game_mode import GameMode


class CountriesMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Countries"

        self.background_image = "assets/background_images/Countries.png"

        self.background_color = "#d9ecff"

        self.word_folder = "countries"