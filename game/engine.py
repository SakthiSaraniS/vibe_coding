import pygame
from .paddle import Paddle
from .ball import Ball
import os

# Game Engine

WHITE = (255, 255, 255)

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
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.winning_score = 5
        self.game_over = False
        self.winner = None
        
        # Initialize sound system
        pygame.mixer.init()
        self.sounds = self.load_sounds()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
    
    def handle_keypress(self, key):
        if self.game_over:
            if key == pygame.K_3:
                self.restart_game(3)
            elif key == pygame.K_5:
                self.restart_game(5)
            elif key == pygame.K_7:
                self.restart_game(7)
            elif key == pygame.K_ESCAPE:
                return False
        return True
    
    def restart_game(self, winning_score):
        self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
    
    def load_sounds(self):
        sounds = {}
        sound_files = {
            'paddle_hit': 'sounds/paddle_hit.wav',
            'wall_bounce': 'sounds/wall_bounce.wav',
            'score': 'sounds/score.wav'
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    sounds[sound_name] = pygame.mixer.Sound(file_path)
                else:
                    sounds[sound_name] = None
            except:
                sounds[sound_name] = None
        
        return sounds
    
    def play_sound(self, sound_name):
        if self.sounds.get(sound_name):
            self.sounds[sound_name].play()

    def update(self):
        if not self.game_over:
            # Handle ball movement and sound
            sound_event = self.ball.move()
            if sound_event:
                self.play_sound(sound_event)
            
            # Handle ball collision and sound
            collision_event = self.ball.check_collision(self.player, self.ai)
            if collision_event:
                self.play_sound(collision_event)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.play_sound('score')
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.play_sound('score')
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)
            
            # Check for game over
            if self.player_score >= self.winning_score:
                self.game_over = True
                self.winner = "Player"
            elif self.ai_score >= self.winning_score:
                self.game_over = True
                self.winner = "AI"

    def render(self, screen):
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
        
        # Draw game over screen
        if self.game_over:
            winner_text = self.big_font.render(f"{self.winner} Wins!", True, WHITE)
            winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2))
            screen.blit(winner_text, winner_rect)
            
            instruction_text = self.font.render("Press 3, 5, 7 for new game or ESC to exit", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(self.width//2, self.height//2 + 80))
            screen.blit(instruction_text, instruction_rect)
