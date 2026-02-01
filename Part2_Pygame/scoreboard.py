import pygame.font


class Scoreboard:
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.screen_rect = screen.get_rect()

        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

    def prep_score(self):
        score_str = str(round(self.stats.score / 10) * 10)
        self.score_img = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def draw_score(self):
        self.screen.blit(self.score_img, self.score_rect)
