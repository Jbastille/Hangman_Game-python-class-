from Game.game_mode import GameMode


class FoodMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Food"

        self.background_image = "assets/background_images/Food.png"

        self.background_color = "#fff0d9"

        self.word_folder = "food"