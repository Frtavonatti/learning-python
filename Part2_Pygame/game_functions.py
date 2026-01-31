from os import stat
import sys
import pygame
from time import sleep

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


def check_play_button(
    settings, screen, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y
):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active_game:
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        # stats.reset_stats()
        ship.ships_left = settings.max_ships
        reset_game(settings, screen, ship, aliens, bullets)
        stats.active_game = True


def check_events(settings, screen, ship, aliens, bullets, stats, play_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                settings,
                screen,
                ship,
                aliens,
                bullets,
                stats,
                play_button,
                mouse_x,
                mouse_y,
            )
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(settings, screen, ship, aliens, bullets, stats, play_button):
    """Update position of all elements on the screen"""
    screen.fill(settings.bg_color)

    if stats.active_game:
        aliens.draw(screen)
        ship.blitme()
        for bullet in bullets.sprites():
            bullet.draw_bullet()
    else:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(settings, screen, bullets, aliens, stats):
    """Update the position of the bullets and get rid of old bullets"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    detect_bullet_alien_collision(settings, screen, aliens, bullets, stats)


def detect_bullet_alien_collision(settings, screen, aliens, bullets, stats):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        stats.score += 1
    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()
        sleep(1)  # momentarily here
        create_fleet(settings, screen, aliens)


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


def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def reset_game(settings, screen, ship, aliens, bullets):
    aliens.empty()
    bullets.empty()
    ship.restart_center()
    ship.ships_left -= 1
    create_fleet(settings, screen, aliens)
    sleep(1)


def ship_hit(settings, screen, stats, ship, aliens, bullets):
    if ship.ships_left > 0:
        reset_game(settings, screen, ship, aliens, bullets)
    else:
        stats.active_game = False
        pygame.mouse.set_visible(True)


def check_alien_ship_collision(settings, screen, stats, ship, aliens, bullets):
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, stats, ship, aliens, bullets)


def check_alien_reached_bottom(settings, screen, stats, ship, aliens, bullets):
    screen_bottom = screen.get_rect().bottom
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_bottom:
            ship_hit(settings, screen, stats, ship, aliens, bullets)
            break


def update_fleet(settings, screen, stats, ship, aliens, bullets):
    """Update fleet position on the screen"""
    check_fleet_edges(settings, aliens)
    aliens.update()
    check_alien_ship_collision(settings, screen, stats, ship, aliens, bullets)
    check_alien_reached_bottom(settings, screen, stats, ship, aliens, bullets)
