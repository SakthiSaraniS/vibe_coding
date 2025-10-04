
import pygame
import math

class Ball:
    def __init__(self, x, y, dx, dy, screen_width, screen_height):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Total speed - keep it constant
        self.speed = math.sqrt(dx**2 + dy**2)
        
        # Max bounce angle in radians (from horizontal)
        self.max_bounce_angle = math.radians(60)  # Reduced from 75 to 60 degrees
        
        # Minimum horizontal speed to prevent too vertical movement
        self.min_horizontal_speed = self.speed * 0.5
        
        # Initialize sounds
        pygame.mixer.init()
        self.sound_paddle = pygame.mixer.Sound("football_goal.wav")
        self.sound_wall = pygame.mixer.Sound("victory_sound.wav")
        self.sound_score = pygame.mixer.Sound("score_count.wav")
        
        # Optional volume adjustment
        self.sound_paddle.set_volume(0.5)
        self.sound_wall.set_volume(0.5)
        self.sound_score.set_volume(0.5)
    
    def move(self):
        """Move the ball and handle wall collision."""
        self.x += self.dx
        self.y += self.dy
        
        # Top wall
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)  # Always bounce downward
            self.sound_wall.play()
        
        # Bottom wall
        elif self.y + self.radius >= self.screen_height:
            self.y = self.screen_height - self.radius
            self.dy = -abs(self.dy)  # Always bounce upward
            self.sound_wall.play()
        
        # Normalize speed after wall bounce to maintain constant speed
        current_speed = math.sqrt(self.dx**2 + self.dy**2)
        if current_speed > 0:
            self.dx = (self.dx / current_speed) * self.speed
            self.dy = (self.dy / current_speed) * self.speed
    
    def check_collision(self, player, ai):
        """Handle paddle collisions with angle-based bounce and prevent sticking."""
        ball_rect = self.rect()
        
        # Player paddle (left side)
        if ball_rect.colliderect(player.rect()) and self.dx < 0:  # Only if moving left
            # Calculate relative intersection (-1 to 1)
            relative_intersect = (self.y - (player.y + player.height / 2)) / (player.height / 2)
            # Clamp to prevent extreme angles
            relative_intersect = max(-0.8, min(0.8, relative_intersect))
            
            # Calculate bounce angle
            bounce_angle = relative_intersect * self.max_bounce_angle
            
            # Set new velocity with constant speed
            self.dx = self.speed * math.cos(bounce_angle)
            self.dy = self.speed * math.sin(bounce_angle)
            
            # Ensure minimum horizontal speed
            if abs(self.dx) < self.min_horizontal_speed:
                sign = 1 if self.dx > 0 else -1
                self.dx = sign * self.min_horizontal_speed
                # Recalculate dy to maintain speed
                self.dy = math.copysign(math.sqrt(self.speed**2 - self.dx**2), self.dy)
            
            # Push ball outside paddle to prevent sticking
            self.x = player.x + player.width + self.radius
            self.sound_paddle.play()
        
        # AI paddle (right side)
        elif ball_rect.colliderect(ai.rect()) and self.dx > 0:  # Only if moving right
            # Calculate relative intersection
            relative_intersect = (self.y - (ai.y + ai.height / 2)) / (ai.height / 2)
            # Clamp to prevent extreme angles
            relative_intersect = max(-0.8, min(0.8, relative_intersect))
            
            # Calculate bounce angle
            bounce_angle = relative_intersect * self.max_bounce_angle
            
            # Set new velocity (negative dx for leftward direction)
            self.dx = -self.speed * math.cos(bounce_angle)
            self.dy = self.speed * math.sin(bounce_angle)
            
            # Ensure minimum horizontal speed
            if abs(self.dx) < self.min_horizontal_speed:
                sign = -1 if self.dx < 0 else 1
                self.dx = sign * self.min_horizontal_speed
                # Recalculate dy to maintain speed
                self.dy = math.copysign(math.sqrt(self.speed**2 - self.dx**2), self.dy)
            
            # Push ball outside paddle
            self.x = ai.x - self.radius
            self.sound_paddle.play()
    
    def reset(self):
        """Reset ball to center with same speed and play score sound."""
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        
        # Reset with horizontal movement only
        direction = -1 if self.dx > 0 else 1  # Reverse horizontal direction
        self.dx = direction * self.speed
        self.dy = 0
        
        self.sound_score.play()
    
    def rect(self):
        """Return ball rectangle for collision detection."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)