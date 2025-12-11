import pygame
import random

class Ground:
    def __init__(self, win_width: int, ground_level: int):
        self.x = 0
        self.y = ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)
        self.color = (240, 240, 240)
    
    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, self.color, self.rect)

class Pipe:
    width = 15
    opening = 100

    def __init__(self, win_width: int, win_height: int, ground_height: int = 100):
        self.x = win_width
        self.top_height = random.randint(50, win_height - 250)
        self.bottom_height = win_height - (self.top_height + self.opening) - ground_height
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.top_height + self.opening, self.width, self.bottom_height)
        self.color = (147, 233, 190)
        self.passed = False
        self.off_screen = False
    
    def draw(self, window: pygame.Surface) -> None:
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        pygame.draw.rect(window, self.color, self.top_rect)
        pygame.draw.rect(window, self.color, self.bottom_rect)

    def move(self, speed: int) -> None:
        self.x -= speed
        if self.x + self.width <= 50:
            self.passed = True
        if self.x + self.width <= 0:
            self.off_screen = True