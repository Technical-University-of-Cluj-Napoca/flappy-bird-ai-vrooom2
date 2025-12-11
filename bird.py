import pygame
import random
from components import Pipe, Ground
from brain import Brain

class Bird:
    def __init__(self, x: int, y: int):
        self.x = 50
        self.y = 200
        self.radius = 10
        self.color = (255, 244, 79)
        self.velocity = 0
        self.isFlapping = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]  # placeholder for inputs
        self.fitness = 0
        self.inputs = 3
        self.brain = Brain(self.inputs)
        self.brain.generate_net()
    
    def flap(self) -> None:
        if not self.isFlapping and not self.sky_collision():
            self.velocity = -6
            self.isFlapping = True

    def update(self, ground: Ground, pipes_list: list[Pipe]) -> None:
        if self.alive:
            if self.velocity >= 0:
                self.isFlapping = False
            self.velocity += 0.25
            self.y += self.velocity
            if self.velocity > 7:
                self.velocity = 7
            
            self.lifespan += 1
        if (self.ground_collision(ground) or self.sky_collision() or self.pipe_collision(pipes_list)):
            self.alive = False
            self.isFlapping = False
            self.velocity = 0

    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    @staticmethod
    def closest_pipe(pipes_list: list[Pipe]) -> Pipe:
        for p in pipes_list:
            if not p.passed:
                return p
            
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
    

    # AI functions

    def look(self, pipes_list: list[Pipe], screen) -> None:
        if pipes_list:
            closest = self.closest_pipe(pipes_list)
            if closest is not None:
                # top pipe gap
                self.vision[0] = max(0, (closest.top_height - self.y) / 620)  # normalized
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x, closest.top_height))
                # distance to pipe
                self.vision[1] = max(0, (closest.x - self.x) / 550)  # normalized
                pygame.draw.line(screen, self.color, (self.x, self.y), (closest.x, self.y))
                # bottom pipe gap
                self.vision[2] = max(0, (closest.top_height + Pipe.opening - self.y) / 620)  # normalized
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x, closest.top_height + Pipe.opening))

    def think(self) -> None:
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.flap()
    
    def calculate_fitness(self) -> None:
        self.fitness = self.lifespan
    
    def clone(self):
        clone = Bird(100, random.randint(50, 570))
        clone.fitness = self.fitness
        clone.color = self.color
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone




    