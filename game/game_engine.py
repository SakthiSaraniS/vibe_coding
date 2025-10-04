import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height, best_of=3, points_to_win_game=5):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Game and series tracking
        self.points_to_win_game = points_to_win_game
        self.current_game_points = {"player": 0, "ai": 0}  # Points in current game
        self.series_score = {"player": 0, "ai": 0}         # Games won in series
        self.best_of = best_of                              # 3,5,7 series

        # Game state
        self.game_over = False
        self.winner_text = ""
        self.game_winner_text = ""  # For showing who won the current game

        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)
        self.ai.auto_track(self.ball, self.height)

        # Check scoring
        if self.ball.x <= 0:
            self.current_game_points["ai"] += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.current_game_points["player"] += 1
            self.ball.reset()

        # Check if current game is won
        if self.current_game_points["player"] >= self.points_to_win_game:
            self.series_score["player"] += 1
            self.game_winner_text = "You won this game!"
            self.reset_round()
        elif self.current_game_points["ai"] >= self.points_to_win_game:
            self.series_score["ai"] += 1
            self.game_winner_text = "AI won this game!"
            self.reset_round()

        # Check series winner
        if self.series_score["player"] > self.best_of // 2:
            self.game_over = True
            self.winner_text = "YOU WIN THE SERIES!"
        elif self.series_score["ai"] > self.best_of // 2:
            self.game_over = True
            self.winner_text = "AI WINS THE SERIES!"

    def reset_round(self):
        """Reset ball and paddles for the next game or next round."""
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        # Reset current game points
        self.current_game_points["player"] = 0
        self.current_game_points["ai"] = 0

    def render(self, screen):
        screen.fill(BLACK)
        if self.game_over:
            # Series winner
            winner_surface = self.font.render(self.winner_text, True, WHITE)
            rect = winner_surface.get_rect(center=(self.width//2, self.height//2))
            screen.blit(winner_surface, rect)

            # Instruction to replay or exit
            info_surface = self.font.render("Press R to Replay or ESC to Exit", True, WHITE)
            info_rect = info_surface.get_rect(center=(self.width//2, self.height//2 + 50))
            screen.blit(info_surface, info_rect)
        else:
            # Draw paddles and ball
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            # Draw current game points
            player_text = self.font.render(f"{self.current_game_points['player']}", True, WHITE)
            ai_text = self.font.render(f"{self.current_game_points['ai']}", True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width*3//4, 20))

            # Draw series score
            series_text = self.font.render(f"Series: {self.series_score['player']} - {self.series_score['ai']}", True, WHITE)
            screen.blit(series_text, (self.width//2 - series_text.get_width()//2, 60))

            # Optional: show last game winner
            if self.game_winner_text:
                game_winner_surface = self.font.render(self.game_winner_text, True, WHITE)
                screen.blit(game_winner_surface, (self.width//2 - game_winner_surface.get_width()//2, 100))
