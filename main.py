import pygame
from game.game_engine import GameEngine
import time
import sys

# Initialize pygame/Start application
pygame.init()
pygame.font.init()  # ensure fonts are ready

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

# Game configuration
WIN_SCORE = 5  # points required to win

# Initialize game engine
engine = GameEngine(WIDTH, HEIGHT)

def show_game_over(screen, winner_text, delay=2.5):
    """
    Draws a translucent overlay with winner_text centered on screen,
    updates display, and waits `delay` seconds so the player can read it.
    """
    # Create fonts
    large_font = pygame.font.SysFont("Arial", 64, bold=True)
    small_font = pygame.font.SysFont("Arial", 20)

    # Create translucent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # black with alpha for translucency

    # Render text
    text_surf = large_font.render(winner_text, True, WHITE)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

    info_surf = small_font.render("Game will close shortly...", True, WHITE)
    info_rect = info_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

    # Blit overlay and text
    screen.blit(overlay, (0, 0))
    screen.blit(text_surf, text_rect)
    screen.blit(info_surf, info_rect)

    pygame.display.flip()

    # Wait while still processing events (avoid unresponsive window)
    start = time.time()
    while time.time() - start < delay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(0.05)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input and update game state
        engine.handle_input()
        engine.update()

        # Check for game-over condition
        if engine.player_score >= WIN_SCORE or engine.ai_score >= WIN_SCORE:
            winner = "PLAYER WINS!" if engine.player_score >= WIN_SCORE else "AI WINS!"
            show_game_over(SCREEN, winner, delay=2.5)
            running = False
            continue

        # Render game objects
        engine.render(SCREEN)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
