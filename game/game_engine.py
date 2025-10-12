import pygame
import os
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

# At very start, before loading sounds
pygame.mixer.pre_init(44100, -16, 2, 256)  # Smaller buffer for lower latency
pygame.init()
# You can centralize sound loading in game_engine or main
_SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "Assets", "Sounds")
paddle_sound = pygame.mixer.Sound(os.path.join(_SOUNDS_DIR, "paddle_hit.wav"))
wall_sound = pygame.mixer.Sound(os.path.join(_SOUNDS_DIR, "paddle_hit.wav"))
point_score_sound = pygame.mixer.Sound(os.path.join(_SOUNDS_DIR, "point_score.wav"))
game_lose_sound = pygame.mixer.Sound(os.path.join(_SOUNDS_DIR, "game_lose.wav"))

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(
            width // 2,
            height // 2,
            7,
            7,
            width,
            height,
            paddle_sound=paddle_sound,
            wall_sound=wall_sound,
            point_score_sound=point_score_sound,
            game_lose_sound=game_lose_sound,
        )

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.pause_font = pygame.font.SysFont("Arial", 48, bold=True)

        self.winning_score = 5
        self.paused = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.paused:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
    
    def handle_pause_input(self):
        """Handle pause/resume input - call this from main loop"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
            elif event.type == pygame.QUIT:
                return "exit"
        return None

    def update(self):
        if not self.paused:
            self.ball.move(self.player, self.ai)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)

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
        
        # Draw pause instruction in bottom-right corner
        instruction_font = pygame.font.SysFont("Arial", 16)
        pause_instruction = instruction_font.render("Press ESC to pause", True, (150, 150, 150))
        screen.blit(pause_instruction, (self.width - pause_instruction.get_width() - 10, 
                                       self.height - pause_instruction.get_height() - 10))
        
        # Draw pause overlay if paused
        if self.paused:
            # Create semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Draw pause text with glow effect
            pause_text = self.pause_font.render("PAUSED", True, (255, 255, 100))
            pause_glow = self.pause_font.render("PAUSED", True, (255, 200, 0))
            
            # Draw glow effect
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        screen.blit(pause_glow, (self.width//2 - pause_text.get_width()//2 + dx, 
                                               self.height//2 - pause_text.get_height()//2 + dy))
            
            screen.blit(pause_text, (self.width//2 - pause_text.get_width()//2, 
                                   self.height//2 - pause_text.get_height()//2))
            
            # Draw instructions
            instruction_font = pygame.font.SysFont("Arial", 24)
            instruction_text = instruction_font.render("Press ESC to resume", True, (200, 200, 200))
            screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, 
                                         self.height//2 + 50))

    def check_game_over_and_replay(self, screen):
        """Check for game over and show replay menu after."""
        winner = None
        if self.player_score >= self.winning_score:
            winner = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner = "AI Wins!"

        if winner:
            # Play a sound once when the game is decided
            try:
                game_lose_sound.play()
            except Exception:
                pass
            popup_width, popup_height = 500, 300
            popup_x = self.width // 2 - popup_width // 2
            popup_y = self.height // 2 - popup_height // 2

            popup_surface = pygame.Surface((popup_width, popup_height))
            popup_surface.fill((20, 20, 20))
            
            # Add gradient background effect
            for i in range(popup_height):
                color_intensity = int(20 + (i / popup_height) * 30)
                pygame.draw.line(popup_surface, (color_intensity, color_intensity, color_intensity), 
                               (0, i), (popup_width, i))

            # Enhanced fonts
            font_large = pygame.font.SysFont("Arial", 48, bold=True)
            font_medium = pygame.font.SysFont("Arial", 28)
            font_small = pygame.font.SysFont("Arial", 24)
            clock = pygame.time.Clock()

            # --- 1️⃣ Display Winner Popup with countdown ---
            countdown = 3
            while countdown > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return "exit"

                popup_surface.fill((20, 20, 20))
                
                # Add gradient background
                for i in range(popup_height):
                    color_intensity = int(20 + (i / popup_height) * 30)
                    pygame.draw.line(popup_surface, (color_intensity, color_intensity, color_intensity), 
                                   (0, i), (popup_width, i))
                
                # Draw border with rounded corners effect
                pygame.draw.rect(popup_surface, (100, 100, 255), popup_surface.get_rect(), 4)
                pygame.draw.rect(popup_surface, (50, 50, 150), (2, 2, popup_width-4, popup_height-4), 2)

                # Winner text with glow effect
                text_surface = font_large.render(winner, True, (255, 255, 100))
                text_glow = font_large.render(winner, True, (255, 200, 0))
                
                # Draw glow effect
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            popup_surface.blit(text_glow, (popup_width // 2 - text_surface.get_width() // 2 + dx, 80 + dy))
                
                popup_surface.blit(text_surface, (popup_width // 2 - text_surface.get_width() // 2, 80))
                
                # Timer with better styling
                timer_text = font_medium.render(f"Next screen in {countdown} sec", True, (200, 255, 200))
                popup_surface.blit(timer_text, (popup_width // 2 - timer_text.get_width() // 2, 160))

                screen.blit(popup_surface, (popup_x, popup_y))
                pygame.display.flip()

                clock.tick(1)
                countdown -= 1

            # --- 2️⃣ Enhanced Replay Menu Popup ---
            selecting = True
            selected_option = 0
            options = [
                ("Best of 3", 2, pygame.K_3),
                ("Best of 5", 3, pygame.K_5), 
                ("Best of 7", 4, pygame.K_7),
                ("Exit Game", -1, pygame.K_ESCAPE)
            ]
            
            while selecting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return "exit"
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return "exit"
                        elif event.key == pygame.K_3:
                            self.winning_score = 2
                            selecting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 3
                            selecting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 4
                            selecting = False
                        elif event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(options)
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(options)
                        elif event.key == pygame.K_RETURN:
                            if options[selected_option][1] == -1:
                                pygame.quit()
                                return "exit"
                            else:
                                self.winning_score = options[selected_option][1]
                                selecting = False

                popup_surface.fill((20, 20, 20))
                
                # Add gradient background
                for i in range(popup_height):
                    color_intensity = int(20 + (i / popup_height) * 30)
                    pygame.draw.line(popup_surface, (color_intensity, color_intensity, color_intensity), 
                                   (0, i), (popup_width, i))
                
                # Draw enhanced border
                pygame.draw.rect(popup_surface, (100, 100, 255), popup_surface.get_rect(), 4)
                pygame.draw.rect(popup_surface, (50, 50, 150), (2, 2, popup_width-4, popup_height-4), 2)

                # Title with glow
                title = font_large.render("Game Over", True, (255, 255, 100))
                title_glow = font_large.render("Game Over", True, (255, 200, 0))
                
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            popup_surface.blit(title_glow, (popup_width // 2 - title.get_width() // 2 + dx, 30 + dy))
                
                popup_surface.blit(title, (popup_width // 2 - title.get_width() // 2, 30))

                # Menu options with highlighting
                y_offset = 100
                for i, (text, score, key) in enumerate(options):
                    if i == selected_option:
                        # Highlighted option
                        pygame.draw.rect(popup_surface, (50, 100, 200), 
                                       (50, y_offset - 5, popup_width - 100, 35))
                        pygame.draw.rect(popup_surface, (100, 150, 255), 
                                       (50, y_offset - 5, popup_width - 100, 35), 2)
                        color = (255, 255, 255)
                    else:
                        color = (200, 200, 200)
                    
                    option_text = font_medium.render(f"{text}", True, color)
                    popup_surface.blit(option_text, (popup_width // 2 - option_text.get_width() // 2, y_offset))
                    y_offset += 40

                # Instructions
                instructions = font_small.render("Use ↑↓ or number keys to select", True, (150, 150, 150))
                popup_surface.blit(instructions, (popup_width // 2 - instructions.get_width() // 2, 250))

                screen.blit(popup_surface, (popup_x, popup_y))
                pygame.display.flip()
                clock.tick(30)

            # --- 3️⃣ Reset game state for new match ---
            self.player_score = 0
            self.ai_score = 0