import pygame
import random
import os

# Initialize the mixer for sound playback
pygame.mixer.init()

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

        # Get absolute path of current file (so sound loading works reliably)
        base_path = os.path.dirname(__file__)

        # Load sound effects from the correct folder
        self.hit_sound = pygame.mixer.Sound(os.path.join(base_path, "hit.wav"))       # paddle hit
        self.bounce_sound = pygame.mixer.Sound(os.path.join(base_path, "bounce.wav")) # wall bounce
        self.score_sound = pygame.mixer.Sound(os.path.join(base_path, "score.mp3"))   # scoring

    def move(self, player, ai):
        # Move ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.bounce_sound.play()

        # Paddle collision detection
        ball_rect = self.rect()
        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
            self.hit_sound.play()
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            self.hit_sound.play()

    def reset(self):
        # Reset ball to center and reverse direction
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.score_sound.play()  # Play scoring sound

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
