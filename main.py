import argparse
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT 
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField, Asteroid
from shot import Shot

def main():
    # Parse optional colemak flag to switch keyboard layout
    parser = argparse.ArgumentParser(description="Run Pygame-Asteroids")
    parser.add_argument("--colemak", action="store_true", help="use Colemak keyboard layout (default is QWERTY)")
    args = parser.parse_args()
    if args.colemak:
        import constants
        constants.CONTROLS = constants.COLEMAK_CONTROLS

    # Initialise the Pygame module
    pygame.init()
    # Initialize font
    font = pygame.font.SysFont(None, 24)
    # Define groups and group members
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    # Setting game resolution
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Creating player and defining starting position based on resolution
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
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
        # Collision detection
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print(f"Game over! Final score: {score}")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += asteroid.split() # Update score dynamically based on split result

        # Refresh the screen
        pygame.display.flip()
        # Pause the game for 1/60th of a second
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
