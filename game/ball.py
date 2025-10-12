import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height

    def check_collision(self, player, ai):
        paddles = [player, ai]
        for paddle in paddles:
            pr = paddle.rect()
            if self.velocity_x < 0 and paddle == ai:
                continue
            if self.velocity_x > 0 and paddle == player:
                continue

            if self.velocity_x > 0:  
                plane_x = pr.left
                start_edge = self.prev_x + self.width
                end_edge = self.x + self.width
            else:  
                plane_x = pr.right
                start_edge = self.prev_x
                end_edge = self.x

            dx = end_edge - start_edge
            if dx == 0:
                continue

            crossed = (start_edge <= plane_x <= end_edge) if self.velocity_x > 0 else (end_edge <= plane_x <= start_edge)
            if not crossed:
                continue

            t = (plane_x - start_edge) / dx
            y_at_hit = self.prev_y + (self.velocity_y * t)

            if pr.top <= y_at_hit + self.height and y_at_hit <= pr.bottom:
                
                self.x = plane_x - self.width if self.velocity_x > 0 else plane_x
                self.velocity_x *= -1

                
                offset = (y_at_hit + self.height / 2 - pr.centery) / (pr.height / 2)
                self.velocity_y += offset * 2.0
                break  

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.prev_x = self.x
        self.prev_y = self.y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
