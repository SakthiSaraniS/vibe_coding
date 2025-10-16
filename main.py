import pygame
from game.game_engine import GameEngine
import time
import sys

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()  # Initialize sound system


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

# Initialize game engine
engine = GameEngine(WIDTH, HEIGHT)

# Default WIN_SCORE
WIN_SCORE = 5

# ================= Helper Functions =================

def show_game_over(screen, winner_text):
    """Show winner overlay and handle replay menu."""
    large_font = pygame.font.SysFont("Arial", 64, bold=True)
    small_font = pygame.font.SysFont("Arial", 20)

    # Overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    
    # Winner text
    text_surf = large_font.render(winner_text, True, WHITE)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))

    # Info text
    info_surf = small_font.render("Press 3, 5, or 7 to replay, or ESC to exit.", True, WHITE)
    info_rect = info_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))

    # Draw
    screen.blit(overlay, (0,0))
    screen.blit(text_surf, text_rect)
    screen.blit(info_surf, info_rect)
    pygame.display.flip()

def replay_menu():
    """
    Wait for user to choose:
    3,5,7 for Best of 3/5/7
    ESC to exit
    Returns WIN_SCORE or None to quit
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    return 3
                elif event.key == pygame.K_5:
                    return 5
                elif event.key == pygame.K_7:
                    return 7
                elif event.key == pygame.K_ESCAPE:
                    return None
        # Small sleep to avoid busy loop
        time.sleep(0.05)

# ================= Main Game Loop =================

def main():
    global WIN_SCORE
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input and update game state
        engine.handle_input()
        engine.update()

        # Check Game Over
        if engine.player_score >= WIN_SCORE or engine.ai_score >= WIN_SCORE:
            winner = "PLAYER WINS!" if engine.player_score >= WIN_SCORE else "AI WINS!"
            show_game_over(SCREEN, winner)

            # Ask player if they want to replay
            choice = replay_menu()
            if choice is None:
                # Exit
                running = False
            else:
                # Reset scores and ball
                WIN_SCORE = choice
                engine.player_score = 0
                engine.ai_score = 0
                engine.ball.reset()
            continue

        # Render game objects
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
