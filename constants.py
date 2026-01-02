import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

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