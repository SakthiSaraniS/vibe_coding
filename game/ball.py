import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            return 'wall_bounce'
        return None

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        
        # Check collision with player paddle
        if ball_rect.colliderect(player.rect()) and self.velocity_x < 0:
            self.velocity_x = abs(self.velocity_x)  # Ensure ball moves away from player
            # Add slight vertical variation based on where ball hits paddle
            hit_pos = (self.y - player.y) / player.height - 0.5
            self.velocity_y += hit_pos * 2
            return 'paddle_hit'
            
        # Check collision with AI paddle  
        elif ball_rect.colliderect(ai.rect()) and self.velocity_x > 0:
            self.velocity_x = -abs(self.velocity_x)  # Ensure ball moves away from AI
            # Add slight vertical variation based on where ball hits paddle
            hit_pos = (self.y - ai.y) / ai.height - 0.5
            self.velocity_y += hit_pos * 2
            return 'paddle_hit'
        
        return None

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
