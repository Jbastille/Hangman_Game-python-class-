from Game.game_mode import GameMode


class CountriesMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Countries"

        self.background_image = "assets/background_images/Countries.png"

        self.background_color = "#d9ecff"

        self.words = [
            ("canada", "North American country"),
            ("brazil", "Famous for football"),
            ("germany", "European country"),
            ("japan", "Island nation in Asia"),
            ("australia", "Country and continent"),
            ("egypt", "Home of the pyramids"),
            ("france", "Known for the Eiffel Tower"),
            ("india", "Second most populated country")
        ]