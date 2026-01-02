import argparse
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, QWERTY_CONTROLS, COLEMAK_CONTROLS, POWERUP_SPEED_COLOR, POWERUP_FIRE_RATE_COLOR, POWERUP_INVINCIBILITY_COLOR, POWERUP_RAPID_FIRE_COLOR, POWERUP_MULTI_SHOT_COLOR
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField, Asteroid
from shot import Shot
from powerupfield import PowerUpField, PowerUp

def main():
    # Parse optional colemak flag to switch keyboard layout
    parser = argparse.ArgumentParser(description="Run Pygame-Asteroids")
    parser.add_argument("--colemak", action="store_true", help="use Colemak keyboard layout (default is QWERTY)")
    args = parser.parse_args()
    
    # Select controls layout based on argument
    controls = COLEMAK_CONTROLS if args.colemak else QWERTY_CONTROLS

    # Initialise the Pygame module
    pygame.init()
    # Initialize font
    font = pygame.font.SysFont(None, 24)
    # Define groups and group members
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    PowerUpField.containers = (updatable,)
    asteroid_field = AsteroidField()
    powerup_field = PowerUpField()
    
    # Setting game resolution
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Creating player and defining starting position based on resolution
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, controls)
    # Setting some variables for in the loop
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    #Print some info to the CLI
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print(f"Using {'Colemak' if args.colemak else 'QWERTY'} controls")
    
    while True:
        # Log information to game_state.json1
        log_state()
        # Close the game when the X is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # Set the background color
        screen.fill("black")
        # Update the position of the ship
        updatable.update(dt)
        # Render the player
        for sprite in drawable:
            sprite.draw(screen)
        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        # Display power-up levels
        y_offset = 40
        speed_text = f"Speed Level: {player.speed_level}"
        speed_display = font.render(speed_text, True, POWERUP_SPEED_COLOR)
        screen.blit(speed_display, (10, y_offset))
        y_offset += 30
        power_text = f"Power Level: {player.power_level}"
        power_display = font.render(power_text, True, POWERUP_FIRE_RATE_COLOR)
        screen.blit(power_display, (10, y_offset))
        y_offset += 30
        multi_shot_text = f"Multi-Shot Level: {player.multi_shot_level}"
        multi_shot_display = font.render(multi_shot_text, True, POWERUP_MULTI_SHOT_COLOR)
        screen.blit(multi_shot_display, (10, y_offset))
        y_offset += 30
        if player.invincibility_timer > 0:
            invincibility_text = f"Invincible: {player.invincibility_timer:.1f}s"
            invincibility_display = font.render(invincibility_text, True, POWERUP_INVINCIBILITY_COLOR)
            screen.blit(invincibility_display, (10, y_offset))
            y_offset += 30
        if player.rapid_fire_timer > 0:
            rapid_fire_text = f"Rapid Fire: {player.rapid_fire_timer:.1f}s"
            rapid_fire_display = font.render(rapid_fire_text, True, POWERUP_RAPID_FIRE_COLOR)
            screen.blit(rapid_fire_display, (10, y_offset))

        # Collision detection
        for asteroid in asteroids:
            if player.collides_with(asteroid) and not player.is_invincible():
                log_event("player_hit")
                print(f"Game over! Final score: {score}, Speed Level: {player.speed_level}, Power Level: {player.power_level}, Multi-Shot Level: {player.multi_shot_level}")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += asteroid.split() # Update score dynamically based on split result

        # Power-up collision detection
        for powerup in powerups:
            if player.collides_with(powerup):
                log_event("powerup_collected")
                player.apply_powerup(powerup.powerup_type)
                powerup.kill()

        # Refresh the screen
        pygame.display.flip()
        # Pause the game for 1/60th of a second
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
