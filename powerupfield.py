import pygame
import random
from powerup import PowerUp
from constants import *

class PowerUpField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, position):
        # Randomly choose power-up type with weights for rarity
        powerup_types = ["speed_upgrade", "fire_rate_upgrade", "invincibility", "rapid_fire", "multi_shot"]
        weights = [1, 1, 1, 1, POWERUP_MULTISHOT_SPAWN_CHANCE]  # multi_shot is half as likely
        powerup_type = random.choices(powerup_types, weights=weights)[0]
        powerup = PowerUp(position.x, position.y, powerup_type)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > POWERUP_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new power-up at a random location on screen
            position = pygame.Vector2(random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
            self.spawn(position)