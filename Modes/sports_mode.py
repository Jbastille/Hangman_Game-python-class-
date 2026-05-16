from Game.game_mode import GameMode


class SportsMode(GameMode):

    def __init__(self):

        super().__init__()

        self.name = "Sports"

        self.background_image = "assets/background_images/Sports.png"

        self.background_color = "#f5d9ff"

        self.words = [
            ("football", "Most popular sport"),
            ("basketball", "Played with hoops"),
            ("tennis", "Played with rackets"),
            ("swimming", "Olympic water sport"),
            ("volleyball", "Played over a net"),
            ("baseball", "Uses bats and bases"),
            ("cricket", "Very popular in India"),
            ("boxing", "Combat sport")
        ]