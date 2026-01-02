import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, controls):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.controls = controls
        # Power-up effects
        self.speed_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.invincibility_timer = 0.0
        self.rapid_fire_timer = 0.0
        # Power-up levels
        self.speed_level = 1
        self.power_level = 1
        self.multi_shot_level = 0

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
        
        if self.multi_shot_level > 0:
            # Multi-shot: fire multiple bullets in a cone
            num_bullets = min(POWERUP_MULTI_SHOT_INITIAL_BULLETS + (self.multi_shot_level - 1) * 2, POWERUP_MULTI_SHOT_MAX_BULLETS)
            total_spread = POWERUP_MULTI_SHOT_BASE_SPREAD + (self.multi_shot_level - 1) * POWERUP_MULTI_SHOT_SPREAD_INCREMENT
            angle_step = total_spread / (num_bullets - 1) if num_bullets > 1 else 0
            start_angle = self.rotation - total_spread / 2
            
            for i in range(num_bullets):
                shot = Shot(self.position.x, self.position.y)
                direction = pygame.Vector2(0, 1).rotate(start_angle + i * angle_step)
                shot.velocity = direction * PLAYER_SHOOT_SPEED
        else:
            # Single shot
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
        color = "grey"
        if self.is_invincible():
            color = POWERUP_INVINCIBILITY_COLOR  # Light blue glow when invincible
        elif self.rapid_fire_timer > 0:
            color = POWERUP_RAPID_FIRE_COLOR  # Cyan glow when rapid fire
        elif self.multi_shot_level > 0:
            color = POWERUP_MULTI_SHOT_COLOR  # Orange glow when multi-shot
        pygame.draw.polygon(screen, color, self.triangle(), LINE_WIDTH)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Use configurable controls for keyboard layout support
        if keys[self.controls["rotate_left"]]:
            self.rotate(-dt)
        if keys[self.controls["rotate_right"]]:
            self.rotate(dt)
        if keys[self.controls["forward"]]:
            self.move(dt)
        if keys[self.controls["back"]]:
            self.move(-dt)
        if keys[self.controls["shoot"]]:
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
        elif powerup_type == "multi_shot":
            self.multi_shot_level = min(self.multi_shot_level + 1, POWERUP_MULTI_SHOT_MAX_BULLETS // 2 + 1)  # max level based on bullets

    def is_invincible(self):
        return self.invincibility_timer > 0