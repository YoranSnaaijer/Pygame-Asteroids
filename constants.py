import pygame
# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Player constants
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200

# Asteroid constants
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Shot constants
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

# Power-up constants
POWERUP_RADIUS = 15
POWERUP_SPAWN_RATE_SECONDS = 5.0
POWERUP_SPEED_UPGRADE = 1.2  # 20% speed increase
POWERUP_FIRE_RATE_UPGRADE = 0.8  # 20% faster firing (multiply cooldown by 0.8)
POWERUP_INVINCIBILITY_DURATION = 5.0
POWERUP_RAPID_FIRE_DURATION = 10.0
POWERUP_MULTISHOT_SPAWN_CHANCE = 0.5  # chance to spawn multi-shot power-up
POWERUP_MULTI_SHOT_DURATION = 15.0
POWERUP_MULTI_SHOT_INITIAL_BULLETS = 2
POWERUP_MULTI_SHOT_MAX_BULLETS = 10
POWERUP_MULTI_SHOT_BASE_SPREAD = 20  # degrees
POWERUP_MULTI_SHOT_SPREAD_INCREMENT = 10  # degrees per level

# Power-up colors
POWERUP_SPEED_COLOR = (0, 255, 0)  # Green
POWERUP_FIRE_RATE_COLOR = (255, 255, 0)  # Yellow
POWERUP_INVINCIBILITY_COLOR = (0, 0, 255)  # Light blue
POWERUP_RAPID_FIRE_COLOR = (0, 255, 255)  # Cyan
POWERUP_MULTI_SHOT_COLOR = (255, 165, 0)  # Orange

# Control mappings for different keyboard layouts
QWERTY_CONTROLS = {
    "rotate_left": pygame.K_a,
    "rotate_right": pygame.K_d,
    "forward": pygame.K_w,
    "back": pygame.K_s,
    "shoot": pygame.K_SPACE,
}

COLEMAK_CONTROLS = {
    "rotate_left": pygame.K_a,
    "rotate_right": pygame.K_s,
    "forward": pygame.K_w,
    "back": pygame.K_r,
    "shoot": pygame.K_SPACE,
}

# Default to QWERTY (WASD)
CONTROLS = QWERTY_CONTROLS