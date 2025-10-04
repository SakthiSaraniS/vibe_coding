import pygame
from game.game_engine import GameEngine
import sys

# Initialize pygame/Start application
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Allow exit after game over
            if engine.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
