import random


class GameMode:

    def __init__(self):

        self.name = "Default"

        self.background_color = "#ffffff"

        self.background_image = None

        self.word_folder = ""

        self.words = []

    # ---------------------------------------------------------
    # LOAD WORDS
    # ---------------------------------------------------------
    def load_words(self, difficulty):

        path = f"data/{self.word_folder}/{difficulty}.txt"

        self.words = []

        with open(path, "r") as file:

            for line in file:

                line = line.strip()

                if ":" in line:

                    word, hint = line.split(":", 1)

                    self.words.append(
                        (word.lower(), hint)
                    )

    # ---------------------------------------------------------
    # RANDOM WORD
    # ---------------------------------------------------------
    def get_random_word(self):

        return random.choice(self.words)