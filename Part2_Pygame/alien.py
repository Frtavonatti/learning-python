import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = ai_settings

        self.image = pygame.image.load("images/alien.bmp")
        self.image.set_colorkey((230, 230, 230))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    # def update(self):

    def blitme(self):
        self.screen.blit(self.image, self.rect)
