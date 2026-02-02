class Stats:
    def __init__(self, settings):
        self.settings = settings
        self.active_game = False
        self.score = 0
        self.level = 1
        self.max_score = 0
        self.ships_left = self.settings.max_ships

        self.read_high_score()

    def read_high_score(self):
        with open("high_score.txt") as file:
            high_score = file.read()
            if high_score:
                self.max_score = int(high_score)
                return int(high_score)

    def write_max_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.max_score))

    def reset_stats(self):
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.max_ships
