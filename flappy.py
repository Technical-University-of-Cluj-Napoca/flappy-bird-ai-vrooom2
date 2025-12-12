import pygame
import sys
import components
from bird import Bird
import population

HEIGHT = 720
WIDTH = 550
BLACK = (12, 12, 12)

bird_images = [pygame.image.load("assets/bird_down.png"),
               pygame.image.load("assets/bird_mid.png"),
               pygame.image.load("assets/bird_up.png")]
skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    ground = components.Ground(WIDTH, HEIGHT - 100, ground_image)
    pipes = []
    #pipes.append(components.Pipe(WIDTH, HEIGHT))
    pipes_spawn_timer = 10

    # bird = Bird(100, (HEIGHT-100) // 2)
    flock = population.Population(100, bird_images)

    while True:
        SCREEN.blit(skyline_image, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         bird.flap()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     bird.flap()
        ground.move(1)
        ground.draw(SCREEN)

        if pipes_spawn_timer <= 0:
            pipes.append(components.Pipe(WIDTH, HEIGHT))
            pipes_spawn_timer = 270
        pipes_spawn_timer -= 1
        for pipe in pipes:
            pipe.move(2)
            pipe.draw(SCREEN, top_pipe_image, bottom_pipe_image)
        for pipe in pipes:
            if pipe.off_screen:
                pipes.remove(pipe)
        if not flock.extinct():
            flock.update_live_birds(ground, pipes, SCREEN)
        else:
            pipes.clear()
            pipes_spawn_timer = 10

            flock.natural_selection()
        # bird.update(ground, pipes)
        # bird.draw(SCREEN)
        # flock.draw(SCREEN)
        
        # if not bird.alive:
        #     SCREEN.blit(game_over_image, ((WIDTH - game_over_image.get_width()) // 2, (HEIGHT - game_over_image.get_height()) // 2))

        CLOCK.tick(60)
        pygame.display.flip()


main()