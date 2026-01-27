class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 46)

        # Ship settings
        self.ship_speed_factor = 0.5
        self.ship_margin = 80  # Margin from screen edges

        # Bullet settings
        self.bullet_speed_factor = 0.5
        self.bullet_width = 3
        self.bullet_heigth = 15
        self.bullet_color = 230, 230, 230
        self.bullet_max = 3

        # Alien settings
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 5
        """fleet_direction of 1 represents right, -1 represents left."""
        self.fleet_direction = 1
