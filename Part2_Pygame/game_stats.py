class Stats:
    def __init__(self, settings):
        self.settings = settings
        self.active_game = False
        self.score = 0
        self.level = 1
        self.max_score = 0
        self.ships_left = self.settings.max_ships

    def reset_stats(self):
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.max_ships
