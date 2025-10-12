import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height,
                 paddle_sound=None, wall_sound=None, 
                 point_score_sound=None, game_lose_sound=None):
        self.original_x = x
        self.original_y = y
        self.x = float(x)
        self.y = float(y)

        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.velocity_x = float(random.choice([-5, 5]))
        self.velocity_y = float(random.choice([-3, 3]))

        self.max_speed = 10.0
        self.speed_increase = 1.05

        # Sound objects (pygame.mixer.Sound)
        self.paddle_sound = paddle_sound
        self.wall_sound = wall_sound
        self.point_score_sound = point_score_sound
        self.game_lose_sound = game_lose_sound
        
        # Sound cooldown to prevent rapid repeated sounds
        self.last_wall_sound_time = 0

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def _apply_paddle_deflection(self, paddle):
        paddle_center = paddle.y + paddle.height / 2
        ball_center = self.y + self.height / 2
        relative = (ball_center - paddle_center) / (paddle.height / 2)
        relative = max(-1.0, min(1.0, relative))

        max_vy = 7.0
        self.velocity_y = relative * max_vy

        new_speed_x = abs(self.velocity_x) * self.speed_increase
        if new_speed_x > self.max_speed:
            new_speed_x = self.max_speed
        self.velocity_x = new_speed_x if self.velocity_x > 0 else -new_speed_x

        # Play paddle hit sound
        if self.paddle_sound:
            self.paddle_sound.play()

    def move(self, player=None, ai=None):
        vx = self.velocity_x
        vy = self.velocity_y

        steps = max(1, int(max(abs(vx), abs(vy))))
        dx = vx / steps
        dy = vy / steps

        for _ in range(steps):
            # Horizontal part
            self.x += dx

            if player and self.rect().colliderect(player.rect()):
                self.x -= dx
                # Ensure ball is outside paddle
                if self.x < player.x + player.width:
                    self.x = player.x + player.width
                self.velocity_x = abs(self.velocity_x)  # Always go right after hitting player paddle
                self._apply_paddle_deflection(player)
                break

            if ai and self.rect().colliderect(ai.rect()):
                self.x -= dx
                # Ensure ball is outside paddle
                if self.x + self.width > ai.x:
                    self.x = ai.x - self.width
                self.velocity_x = -abs(self.velocity_x)  # Always go left after hitting AI paddle
                self._apply_paddle_deflection(ai)
                break

            # Vertical part
            self.y += dy
            if self.y <= 0:
                self.y = 0
                # reverse vy
                self.velocity_y = abs(self.velocity_y)
                # Play wall sound with cooldown to prevent lag
                current_time = pygame.time.get_ticks()
                if self.wall_sound and current_time - self.last_wall_sound_time > 100:
                    self.wall_sound.play()
                    self.last_wall_sound_time = current_time
            elif self.y + self.height >= self.screen_height:
                self.y = self.screen_height - self.height
                self.velocity_y = -abs(self.velocity_y)
                # Play wall sound with cooldown to prevent lag
                current_time = pygame.time.get_ticks()
                if self.wall_sound and current_time - self.last_wall_sound_time > 100:
                    self.wall_sound.play()
                    self.last_wall_sound_time = current_time

    def reset(self):
        self.x = float(self.original_x)
        self.y = float(self.original_y)
        self.velocity_x *= -1
        self.velocity_y = float(random.choice([-3, 3]))
        # play point score sound
        if self.point_score_sound:
            self.point_score_sound.play()
