import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    WIN_SCORE = 5  # First to 5 wins

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winner_text = ""

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return  # Stop updating after game over

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)
        self.ai.auto_track(self.ball, self.height)

        # Score logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Check winner
        if self.player_score >= self.WIN_SCORE:
            self.game_over = True
            self.winner_text = "YOU WIN!"
        elif self.ai_score >= self.WIN_SCORE:
            self.game_over = True
            self.winner_text = "AI WINS!"

    def render(self, screen):
        screen.fill(BLACK)
        if self.game_over:
            # Display winner
            winner_surface = self.font.render(self.winner_text, True, WHITE)
            rect = winner_surface.get_rect(center=(self.width//2, self.height//2))
            screen.blit(winner_surface, rect)
        else:
            # Draw paddles and ball
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            # Draw score
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))
