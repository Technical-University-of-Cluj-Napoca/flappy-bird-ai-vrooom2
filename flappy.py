import pygame
import sys
import components
from bird import Bird
import population

HEIGHT = 720
WIDTH = 550
BLACK = (12, 12, 12)

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    ground = components.Ground(WIDTH, HEIGHT - 100)
    pipes = []
    #pipes.append(components.Pipe(WIDTH, HEIGHT))
    pipes_spawn_timer = 10

    bird = Bird(100, (HEIGHT-100) // 2)
    # flock = population.Population(10)

    while True:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
        
        ground.draw(SCREEN)

        if pipes_spawn_timer <= 0:
            pipes.append(components.Pipe(WIDTH, HEIGHT))
            pipes_spawn_timer = 270
        pipes_spawn_timer -= 1
        for pipe in pipes:
            pipe.draw(SCREEN)
            pipe.move(1)
        for pipe in pipes:
            if pipe.off_screen:
                pipes.remove(pipe)
        bird.update(ground, pipes)
        bird.draw(SCREEN)
        # flock.draw(SCREEN)
        
        CLOCK.tick(60)
        pygame.display.flip()


main()