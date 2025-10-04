import pygame
from game.game_engine import GameEngine
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT, best_of=3)  # Example: Best of 3

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if engine.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset series
                    engine.player_score = 0
                    engine.ai_score = 0
                    engine.rounds_played = 0
                    engine.game_over = False
                    engine.winner_text = ""
                    engine.reset_round()

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
