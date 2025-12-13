import pygame
import sys
import components
from bird import Bird
import population

HEIGHT = 720
WIDTH = 550
BLACK = (12, 12, 12)
WHITE = (255, 255, 255)
ORANGE = (255, 155, 0)
FONT_NAME = 'Arial'

BRONZE = (205, 127, 50)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
PLATINUM = (229, 228, 226)

bird_images = [pygame.image.load("assets/bird_down.png"),
               pygame.image.load("assets/bird_mid.png"),
               pygame.image.load("assets/bird_up.png")]
skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

top_pipe_base = pygame.transform.scale(top_pipe_image, (52, top_pipe_image.get_height()))
bottom_pipe_base = pygame.transform.scale(bottom_pipe_image, (52, bottom_pipe_image.get_height()))

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 30, bold=True)
    small_font = pygame.font.SysFont(FONT_NAME, 20, bold=True)

    ground = components.Ground(WIDTH, HEIGHT - 100, ground_image)
    pipes = []
    #pipes.append(components.Pipe(WIDTH, HEIGHT))
    pipes_spawn_timer = 10
    score = 0
    game_state = "MENU"
    mode = "MANUAL"
    show_popup = False
    manual_high_score = 0
    auto_high_score = 0

    bird = None
    flock = None

    def reset_game(new_mode):
        nonlocal bird, flock, pipes, score, pipes_spawn_timer
        pipes.clear()
        pipes_spawn_timer = 10
        score = 0

        if new_mode == "MANUAL":
            bird = Bird(100, (HEIGHT-100) // 2, bird_images)
            flock = None
        else:
            flock = population.Population(50, bird_images)
            bird = None

    while True:
        SCREEN.blit(skyline_image, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_state == "GAME" and mode == "MANUAL":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bird.flap()
            if game_state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                if show_popup:
                    show_popup = False
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                        if 300 < mouse_y < 350:
                            game_state = "GAME"
                            mode = "MANUAL"
                            reset_game(mode)
                        elif 370 < mouse_y < 420:
                            game_state = "GAME"
                            mode = "AUTO"
                            reset_game(mode)
                        elif 440 < mouse_y < 490:
                            show_popup = True
            if game_state == "GAMEOVER" and event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "MENU"
        if game_state == "MENU":
            ground.move(1)
            ground.draw(SCREEN)
            SCREEN.blit(start_image, (WIDTH//2 - start_image.get_width() // 2, 100))
            pygame.draw.rect(SCREEN, (200, 200, 200), (WIDTH//2 - 100, 300, 200, 50), border_radius=10)
            pygame.draw.rect(SCREEN, (200, 200, 200), (WIDTH//2 - 100, 370, 200, 50), border_radius=10)
            pygame.draw.rect(SCREEN, (200, 200, 200), (WIDTH//2 - 100, 440, 200, 50), border_radius=10)

            man_text = font.render("Manual Mode", True, BLACK)
            auto_text = font.render("Auto Mode", True, BLACK)
            score_text = font.render("Highest Score", True, BLACK)
            copyright_text = font.render("(c) .vrooom2", True, ORANGE)
            SCREEN.blit(man_text, (WIDTH//2 - man_text.get_width() // 2, 310))
            SCREEN.blit(auto_text, (WIDTH//2 - auto_text.get_width() // 2, 380))
            SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width() // 2, 450))
            SCREEN.blit(copyright_text, (WIDTH//2 - copyright_text.get_width() // 2, 510))
            if show_popup:
                popup_rect = pygame.Rect(WIDTH//2 - 150, 200, 300, 200)
                pygame.draw.rect(SCREEN, WHITE, popup_rect, border_radius=15)
                pygame.draw.rect(SCREEN, BLACK, popup_rect, 3, border_radius=15)
                title = font.render("Highest Scores", True, BLACK)
                manual_score_text = font.render(f"Manual: {manual_high_score}", True, BLACK)
                auto_score_text = font.render(f"Auto: {auto_high_score}", True, BLACK)
                close_text = small_font.render("Click to Close", True, (100, 100, 100))

                SCREEN.blit(title, (WIDTH//2 - title.get_width() // 2, 220))
                SCREEN.blit(manual_score_text, (WIDTH//2 - manual_score_text.get_width()//2, 270))
                SCREEN.blit(auto_score_text, (WIDTH//2 - auto_score_text.get_width()//2, 310))
                SCREEN.blit(close_text, (WIDTH//2 - close_text.get_width()//2, 370))
        elif game_state == "GAME":
            ground.move(1)
            ground.draw(SCREEN)

            if pipes_spawn_timer <= 0:
                pipes.append(components.Pipe(WIDTH, HEIGHT,top_pipe_image, bottom_pipe_image))
                pipes_spawn_timer = 150
            pipes_spawn_timer -= 1
            for pipe in pipes:
                pipe.move(2)
                pipe.draw(SCREEN)
                if not pipe.passed and pipe.x + pipe.width < 100:
                    score += 1
                    pipe.passed = True
                    
            for pipe in pipes[:]:
                if pipe.off_screen:
                    pipes.remove(pipe)
            if mode == "AUTO":
                if not flock.extinct():
                    flock.update_live_birds(ground, pipes, SCREEN)
                else:
                    if score > auto_high_score:
                        auto_high_score = score
                    pipes.clear()
                    pipes_spawn_timer = 10
                    score = 0
                    flock.natural_selection()
            elif mode == "MANUAL":
                bird.update(ground, pipes)
                bird.draw(SCREEN)
                if not bird.alive or bird.ground_collision(ground) or bird.pipe_collision(pipes):
                    game_state = "GAMEOVER"
                    if score > manual_high_score:
                        manual_high_score = score
            score_text = font.render(f"Score: {score}", True, BLACK)
            SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 50))
        elif game_state == "GAMEOVER":
            ground.draw(SCREEN)
            for pipe in pipes:
                pipe.draw(SCREEN)
            if mode == "MANUAL":
                bird.draw(SCREEN)
            SCREEN.blit(game_over_image, ((WIDTH - game_over_image.get_width()) // 2, HEIGHT // 2 - 150))

            panel_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 120)
            pygame.draw.rect(SCREEN, WHITE, panel_rect, border_radius=10)
            pygame.draw.rect(SCREEN, BLACK, panel_rect, 3, border_radius=10)

            current_score_text = font.render(f"Score: {score}", True, BLACK)
            if mode == "MANUAL":
                best_score = manual_high_score
            else:
                best_score = auto_high_score
            best_score_text = font.render(f"Best: {best_score}", True, BLACK)
            SCREEN.blit(current_score_text, (panel_rect.centerx - current_score_text.get_width()//2, panel_rect.y + 20))
            SCREEN.blit(best_score_text, (panel_rect.centerx - best_score_text.get_width()//2, panel_rect.y + 60))
            draw_medal(SCREEN, score, panel_rect.x + 30, panel_rect.centery)

            restart_text = small_font.render("Click to return to Menu", True, WHITE)
            text_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
            pygame.draw.rect(SCREEN, BLACK, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10), border_radius=5)
            SCREEN.blit(restart_text, text_rect)

        CLOCK.tick(60)
        pygame.display.flip()

def draw_medal(screen, score, x, y):
    color = None
    if score >= 40:
        color = PLATINUM
    elif score >= 30:
        color = GOLD
    elif score >= 20:
        color = SILVER
    elif score >= 10:
        color = BRONZE
    if color:
        pygame.draw.circle(screen, color, (x, y), 20)
        pygame.draw.circle(screen, BLACK, (x, y), 20, 2)
main()