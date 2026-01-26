import sys
import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(settings, screen, ship, aliens, bullets):
    """Update position of all elements on the screen"""
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    aliens.draw(screen)
    ship.blitme()

    # Make the most recently drawn screen visible
    pygame.display.flip()


# Delete bullets that are out of viewport
def update_bullets(bullets):
    """Update the position of the bullets and get rid of old bullets"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)


def fire_bullets(settings, screen, ship, bullets):
    """Fire a bullet if bullet limit not reached yet"""
    if len(bullets) < settings.bullet_max:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens(settings, alien_width):
    """Determine the number of aliens that fit the row"""
    available_space = settings.screen_width - alien_width * 2
    number_of_aliens = int(available_space / (alien_width * 2))
    return number_of_aliens


def get_number_rows(settings, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space = settings.screen_height - (alien_height * 3) - settings.ship_margin
    number_of_rows = int(available_space / (2 * alien_height))
    return number_of_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    """Create a single alien"""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    # Position
    alien.x += alien_width * 2 * alien_number
    alien.y += alien_height * 2 * row_number
    alien.rect.x = int(alien.x)
    alien.rect.y = int(alien.y)

    aliens.add(alien)


def create_fleet(settings, screen, aliens):
    """Create a full fleet of aliens"""
    alien = Alien(settings, screen)
    number_rows = get_number_rows(settings, alien.rect.height)
    number_aliens_x = get_number_aliens(settings, alien.rect.width)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien = create_alien(settings, screen, aliens, alien_number, row_number)
