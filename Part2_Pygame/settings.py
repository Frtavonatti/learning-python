class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 46)

        # Ship settings
        self.ship_margin = 80  # Margin from screen edges
        self.max_ships = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_heigth = 15
        self.bullet_color = 230, 230, 230
        self.bullet_max = 3

        # Alien settings
        self.fleet_drop_speed = 5

        # Increase game speed factor
        self.speed_up_scale = 1.1

        # Testing values
        # self.bullet_width = self.screen_width / 3

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1

        """fleet_direction of 1 represents right, -1 represents left."""
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
