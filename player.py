import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, CONTROLS, SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_SPEED_UPGRADE, POWERUP_FIRE_RATE_UPGRADE, POWERUP_INVINCIBILITY_DURATION, POWERUP_RAPID_FIRE_DURATION
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        # Power-up effects
        self.speed_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.invincibility_timer = 0.0
        self.rapid_fire_timer = 0.0
        # Power-up levels
        self.speed_level = 1
        self.power_level = 1

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * self.speed_multiplier * dt
        self.position += rotated_with_speed_vector
        
    def shoot(self):
        effective_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS * self.fire_rate_multiplier
        if self.rapid_fire_timer > 0:
            effective_cooldown *= 0.5  # Rapid fire makes it twice as fast
        if self.cooldown > 0:
            return
        self.cooldown = effective_cooldown
        shot = Shot(self.position.x, self.position.y)
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED

    def apply_powerup(self, powerup_type):
        if powerup_type == "speed_upgrade":
            self.speed_multiplier *= POWERUP_SPEED_UPGRADE
        elif powerup_type == "fire_rate_upgrade":
            self.fire_rate_multiplier *= POWERUP_FIRE_RATE_UPGRADE
        elif powerup_type == "invincibility":
            self.invincibility_timer = POWERUP_INVINCIBILITY_DURATION
        elif powerup_type == "rapid_fire":
            self.rapid_fire_timer = POWERUP_RAPID_FIRE_DURATION

    def is_invincible(self):
        return self.invincibility_timer > 0

    def draw(self, screen):
        color = "blue"
        if self.is_invincible():
            color = "yellow"  # Glow when invincible
        elif self.rapid_fire_timer > 0:
            color = "cyan"  # Glow when rapid fire
        pygame.draw.polygon(screen, color, self.triangle(), LINE_WIDTH)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Use configurable controls for keyboard layout support
        if keys[CONTROLS["rotate_left"]]:
            self.rotate(-dt)
        if keys[CONTROLS["rotate_right"]]:
            self.rotate(dt)
        if keys[CONTROLS["forward"]]:
            self.move(dt)
        if keys[CONTROLS["back"]]:
            self.move(-dt)
        if keys[CONTROLS["shoot"]]:
            self.shoot()
        
        self.cooldown -= dt
        
        # Update power-up timers
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= dt
        
        # Screen wrapping
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

    def apply_powerup(self, powerup_type):
        if powerup_type == "speed_upgrade":
            self.speed_multiplier *= POWERUP_SPEED_UPGRADE
            self.speed_level += 1
        elif powerup_type == "fire_rate_upgrade":
            self.fire_rate_multiplier *= POWERUP_FIRE_RATE_UPGRADE
            self.power_level += 1
        elif powerup_type == "invincibility":
            self.invincibility_timer = POWERUP_INVINCIBILITY_DURATION
        elif powerup_type == "rapid_fire":
            self.rapid_fire_timer = POWERUP_RAPID_FIRE_DURATION

    def is_invincible(self):
        return self.invincibility_timer > 0