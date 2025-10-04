import pygame
from game.game_engine import GameEngine
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")
clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont("Arial", 40)

def choose_best_of():
    """Show menu to choose Best of 3, 5, or 7."""
    choosing = True
    best_of = 3  # default
    while choosing:
        SCREEN.fill((0, 0, 0))
        title = FONT.render("Choose Series: 3, 5, or 7 (Press 3/5/7)", True, (255, 255, 255))
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    best_of = 3
                    choosing = False
                elif event.key == pygame.K_5:
                    best_of = 5
                    choosing = False
                elif event.key == pygame.K_7:
                    best_of = 7
                    choosing = False
    return best_of

def main():
    best_of = choose_best_of()
    engine = GameEngine(WIDTH, HEIGHT, best_of=best_of)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle replay or exit
            if engine.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Replay: choose series again
                    best_of = choose_best_of()
                    engine = GameEngine(WIDTH, HEIGHT, best_of=best_of)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
