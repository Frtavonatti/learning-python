import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.screen_rect = screen.get_rect()

        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_level()
        self.prep_max_score()
        self.prep_ships()

    def prep_score(self):
        score_str = str(round(self.stats.score / 10) * 10)

        self.score_img = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        level_str = str(self.stats.level)

        self.level_img = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 20

    def prep_max_score(self):
        max_score_str = str(round(self.stats.max_score / 10) * 10)
        self.max_score_img = self.font.render(
            max_score_str, True, self.text_color, self.settings.bg_color
        )

        self.max_score_rect = self.max_score_img.get_rect()
        self.max_score_rect.centerx = self.screen_rect.centerx
        self.max_score_rect.top = 20

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 20
            self.ships.add(ship)

    def draw_score(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.screen.blit(self.max_score_img, self.max_score_rect)
        self.ships.draw(self.screen)
