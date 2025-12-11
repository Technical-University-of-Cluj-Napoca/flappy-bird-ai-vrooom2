import pygame
import random
from components import Pipe, Ground

class Bird:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 244, 79)
        self.velocity = 0
        self.isFlapping = False
        self.alive = True

        # AI
        self.decision = None
    
    def flap(self) -> None:
        if not self.isFlapping and not self.sky_collision():
            self.velocity = -5
            self.isFlapping = True

    def update(self, ground: Ground, pipes_list: list[Pipe]) -> None:
        if not (self.ground_collision(ground) or self.sky_collision() or self.pipe_collision(pipes_list)):
            if self.velocity >= 0:
                self.isFlapping = False
            self.velocity += 0.25
            self.y += self.velocity
            if self.velocity > 5:
                self.velocity = 5
        else:
            self.alive = False
            self.isFlapping = False
            self.velocity = 0

    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def ground_collision(self, ground: Ground) -> bool:
        return self.get_rect().colliderect(ground.rect)

    def sky_collision(self) -> bool: # to check
        return self.y - self.radius <= 10

    def pipe_collision(self, pipe_list: list[Pipe]) -> bool:
        bird_rect = self.get_rect()
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
                return True
        return False