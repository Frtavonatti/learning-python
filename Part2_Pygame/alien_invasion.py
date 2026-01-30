from os import stat
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import Stats
from button import Button
import game_functions as gf


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    stats = Stats(ai_settings)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    play_button = Button(screen, "Start")

    gf.create_fleet(ai_settings, screen, aliens)

    ship.ships_left -= 1

    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button)

        if stats.active_game:
            ship.update()
            gf.update_bullets(ai_settings, screen, bullets, aliens, stats)
            gf.update_fleet(ai_settings, screen, stats, ship, aliens, bullets)


run_game()
