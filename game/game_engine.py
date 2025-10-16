import pygame
from .paddle import Paddle
from .ball import Ball

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # default to Best of 5

        self.game_over = False
        self.winner_text = ""

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Skip updates if in game over menu
        if self.game_over:
            return

        self.ball.move(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI follows the ball
        self.ai.auto_track(self.ball, self.height)

        # Check if game over
        self.check_game_over()

    def render(self, screen):
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # Show winner and replay options
        if self.game_over:
            self.show_replay_menu(screen)

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "AI Wins!"

    def show_replay_menu(self, screen):
        """Display Game Over and Replay options."""
        # Draw winner message
        winner_surface = self.large_font.render(self.winner_text, True, WHITE)
        text_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 3))
        screen.blit(winner_surface, text_rect)

        # Draw options
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit",
        ]

        for i, option in enumerate(options):
            opt_surface = self.font.render(option, True, WHITE)
            opt_rect = opt_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            screen.blit(opt_surface, opt_rect)

        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.start_new_game(3)
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.start_new_game(5)
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.start_new_game(7)
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

    def start_new_game(self, best_of):
        """Reset scores, ball, and paddles for a new game."""
        self.winning_score = best_of
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.game_over = False
