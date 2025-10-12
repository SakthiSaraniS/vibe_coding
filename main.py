import pygame
from game.game_engine import GameEngine
# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        
        # Handle pause input and other events
        result = engine.handle_pause_input()
        if result == "exit":
            running = False
            continue

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        # Check for game over + replay logic
        result = engine.check_game_over_and_replay(SCREEN)
        if result == "exit":
            running = False
        elif result == "replay":
            continue

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
