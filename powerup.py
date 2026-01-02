import pygame
import random
from circleshape import CircleShape
from constants import *

class PowerUp(CircleShape):
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, POWERUP_RADIUS)
        self.powerup_type = powerup_type
        # Set color based on type
        if powerup_type == "speed_upgrade":
            self.color = POWERUP_SPEED_COLOR
        elif powerup_type == "fire_rate_upgrade":
            self.color = POWERUP_FIRE_RATE_COLOR
        elif powerup_type == "invincibility":
            self.color = POWERUP_INVINCIBILITY_COLOR
        elif powerup_type == "rapid_fire":
            self.color = POWERUP_RAPID_FIRE_COLOR
        elif powerup_type == "multi_shot":
            self.color = POWERUP_MULTI_SHOT_COLOR
        else:
            self.color = (255, 255, 255)  # White

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        # Power-ups don't move, they stay in place
        pass