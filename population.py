import bird
import random

class Population:
    def __init__(self, size):
        self.birds = [bird.Bird(100, random.randint(50, 570)) for _ in range(size)]
        for b in self.birds:
            b.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def update(self):
        for b in self.birds:
            b.update()
    
    def draw(self, window):
        for b in self.birds:
            b.draw(window)