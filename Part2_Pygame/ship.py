import pygame


class Ship:
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        # Cache frequently used settings
        self.speed = ai_settings.ship_speed_factor
        self.margin = ai_settings.ship_margin

        self.image = pygame.image.load("images/ship.bmp")
        self.image.set_colorkey((230, 230, 230))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Position
        self.rect.bottom = self.screen_rect.bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.rect.bottom - self.margin

        # Use float for smooth movement
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # State
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if (
            self.moving_right
            and self.rect.centerx < self.screen_rect.right - self.margin
        ):
            self.center_x += self.speed
        elif self.moving_left and self.rect.centerx > self.margin:
            self.center_x -= self.speed

        elif self.moving_up and self.rect.centery > self.margin:
            self.center_y -= self.speed
        elif (
            self.moving_down
            and self.rect.centery < self.screen_rect.bottom - self.margin
        ):
            self.center_y += self.speed

        # Convert float positions to integers for pixel-perfect rendering
        # (Rect coordinates must be integers; we keep floats to preserve sub-pixel accuracy)
        self.rect.centerx = int(self.center_x)
        self.rect.centery = int(self.center_y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
