import pygame
from .paddle import Paddle
from .ball import Ball

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

        self.player_score = 0
        self.ai_score = 0
        self.max_score = 5

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.game_over = False
        self.waiting_for_replay = False
        self.winner = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        if self.game_over or self.waiting_for_replay:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        self.check_game_over()

    def check_game_over(self):
        if self.player_score >= self.max_score:
            self.winner = "Player"
            self.game_over = True
            self.waiting_for_replay = True
        elif self.ai_score >= self.max_score:
            self.winner = "AI"
            self.game_over = True
            self.waiting_for_replay = True

    def render(self, screen):
        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            message = f"{self.winner} Wins!"
            text_surface = self.big_font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 60))
            screen.blit(text_surface, text_rect)

        if self.waiting_for_replay:
            options = "Press 3, 5, or 7 for Best Of • ESC to Exit"
            opt_surface = self.small_font.render(options, True, WHITE)
            opt_rect = opt_surface.get_rect(center=(self.width // 2, self.height // 2 + 20))
            screen.blit(opt_surface, opt_rect)

    def handle_replay_input(self):
        keys = pygame.key.get_pressed()

        if not self.waiting_for_replay:
            return False  

        if keys[pygame.K_3]:
            self.start_new_match(3)
        elif keys[pygame.K_5]:
            self.start_new_match(5)
        elif keys[pygame.K_7]:
            self.start_new_match(7)
        elif keys[pygame.K_ESCAPE]:
            return True  
        return False  

    def start_new_match(self, best_of):
        self.max_score = best_of
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.waiting_for_replay = False
        self.winner = None
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2

    def is_game_over(self):
        return self.game_over

    def is_waiting_for_replay(self):
        return self.waiting_for_replay
