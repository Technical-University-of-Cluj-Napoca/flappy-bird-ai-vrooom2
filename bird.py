import pygame
import random
from components import Pipe, Ground

class Bird:
    def __init__(self, x: int, y: int, images: list):
        self.x = x
        self.y = y
        self.images = images
        self.image = self.images[0]
        self.img_index = 0
        self.radius = 15
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
        self.img_index += 1
        if self.img_index < 5:
            self.image = self.images[0]
        elif self.img_index < 10:
            self.image = self.images[1]
        elif self.img_index < 15:
            self.image = self.images[2]
        elif self.img_index < 20:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
            self.img_index = 0

        if self.velocity < 0:
            rotated_image = pygame.transform.rotate(self.image, 25)
        elif self.velocity > 2:
            rotated_image = pygame.transform.rotate(self.image, -25)
        else:
            rotated_image = self.image

        rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, rect.topleft)

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