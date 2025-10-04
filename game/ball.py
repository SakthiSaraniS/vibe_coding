import pygame

WHITE = (255, 255, 255)

class Ball:
    def __init__(self, x, y, dx, dy, screen_width, screen_height):
        self.x = x
        self.y = y
        self.dx = dx   # speed in x
        self.dy = dy   # speed in y
        self.radius = 10
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        """Move the ball with boundary check."""
        self.x += self.dx
        self.y += self.dy

        # Wall collision (top and bottom)
        if self.y - self.radius <= 0 or self.y + self.radius >= self.screen_height:
            self.dy = -self.dy

    def check_collision(self, player, ai):
        """Check for collision with paddles and adjust bounce."""
        ball_rect = self.rect()

        # Player paddle collision
        if ball_rect.colliderect(player.rect()):
            self.dx = abs(self.dx)  # ensure ball goes right
            # bounce angle based on hit position
            offset = (self.y - (player.y + player.height // 2)) / (player.height // 2)
            self.dy = offset * 7  # adjust angle

        # AI paddle collision
        if ball_rect.colliderect(ai.rect()):
            self.dx = -abs(self.dx)  # ensure ball goes left
            offset = (self.y - (ai.y + ai.height // 2)) / (ai.height // 2)
            self.dy = offset * 7

    def reset(self):
        """Reset ball to center."""
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.dx = -self.dx  # reverse direction
        self.dy = 0

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)
