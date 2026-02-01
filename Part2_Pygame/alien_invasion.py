import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import Stats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf


def run_game():
    pygame.init()
    settings = Settings()
    settings.initialize_dynamic_settings()

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    stats = Stats(settings)
    sb = Scoreboard(settings, screen, stats)
    ship = Ship(settings, screen)
    bullets = Group()
    aliens = Group()
    play_button = Button(screen, "Start")

    gf.create_fleet(settings, screen, aliens)
    sb.prep_score()

    ship.ships_left -= 1

    while True:
        gf.check_events(settings, screen, ship, aliens, bullets, stats, play_button)
        gf.update_screen(
            settings, screen, ship, aliens, bullets, stats, play_button, sb
        )

        if stats.active_game:
            ship.update()
            gf.update_bullets(settings, screen, bullets, aliens, stats, sb)
            gf.update_fleet(settings, screen, stats, ship, aliens, bullets)


run_game()
