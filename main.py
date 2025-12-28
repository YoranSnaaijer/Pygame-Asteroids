import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT 
from logger import log_state
from player import Player

def main():
    #Initialise the Pygame module
    pygame.init()
    # Setting game resolution
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Setting player starting position based on resolution
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    # Setting some variables for in the loop
    clock = pygame.time.Clock()
    dt = 0
    #Print some info to the CLI
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(F"Screen height: {SCREEN_HEIGHT}")

    while True:
        # Log information to game_state.json1
        log_state()
        # Close the game when the X is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # Set the background color
        screen.fill("black")
        player.draw(screen)
        # Refresh the screen
        pygame.display.flip()
        # Pause the game for 1/60th of a second
        clock.tick(60)
        
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
