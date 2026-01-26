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
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    aliens.draw(screen)
    ship.blitme()

    # Make the most recently drawn screen visible
    pygame.display.flip()


# Delete bullets that are out of viewport
def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)


def fire_bullets(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_max:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens(settings, alien_width):
    available_space = settings.screen_width - alien_width * 2
    number_of_aliens = int(available_space / (alien_width * 2))
    return number_of_aliens


def create_alien(settings, screen, aliens, alien_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x += alien_width * 2 * alien_number
    alien.rect.x = int(alien.x)
    aliens.add(alien)


def create_fleet(settings, screen, aliens):
    alien = Alien(settings, screen)
    number_of_aliens = get_number_aliens(settings, alien.rect.width)

    for alien_number in range(number_of_aliens):
        alien = create_alien(settings, screen, aliens, alien_number)
