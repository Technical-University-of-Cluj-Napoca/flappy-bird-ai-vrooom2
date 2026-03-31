import pygame
import random

class Ground:
    def __init__(self, win_width: int, ground_level: int, image: pygame.Surface):
        self.x = 0
        self.y = ground_level
        self.image = image
        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.rect = pygame.Rect(self.x, self.y, win_width, 100)

    def move(self, speed: int):
        self.x1 -= speed
        self.x2 -= speed
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
    
    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, (self.x1, self.y))
        window.blit(self.image, (self.x2, self.y))

class Pipe:
    width = 52
    opening = 150

    def __init__(self, win_width: int, win_height: int, top_img, bottom_img, ground_height: int = 100):
        self.x = win_width
        self.top_height = random.randint(50, win_height - ground_height - self.opening - 50)
        self.bottom_height = win_height - (self.top_height + self.opening) - ground_height
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.top_height + self.opening, self.width, self.bottom_height)
        self.passed = False
        self.off_screen = False
        self.top_pipe_img = top_img.subsurface((0, top_img.get_height() - self.top_height, 52, self.top_height))
        self.bottom_pipe_img = bottom_img.subsurface((0, 0, 52, self.bottom_height))
    
    def draw(self, window: pygame.Surface) -> None:
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        window.blit(self.top_pipe_img, (self.x, 0))
        window.blit(self.bottom_pipe_img, (self.x, self.top_height + self.opening))

    def move(self, speed: int) -> None:
        self.x -= speed
        if self.x + self.width <= 50:
            self.passed = True
        if self.x + self.width <= 0:
            self.off_screen = True