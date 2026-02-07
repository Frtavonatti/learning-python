import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, settings, screen, ship):
        super().__init__()

        self.screen = screen
        self.settings = settings
        self.color = self.settings.bullet_color
        self.width = self.settings.bullet_width
        self.heigth = self.settings.bullet_heigth
        self.speed = self.settings.bullet_speed_factor

        self.rect = pygame.Rect(0, 0, self.width, self.heigth)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
