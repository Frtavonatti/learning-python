class Stats:
    def __init__(self, settings):
        self.settings = settings
        self.active_game = True
        self.score = 0

    def reset_stats(self):
        self.ships_left = self.settings.max_ships
