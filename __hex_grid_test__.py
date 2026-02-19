import pygame
import math
import scripts.hex_grid as grid


pygame.init()

game_window_width, game_window_height = [1280,720]

screen = pygame.display.set_mode((game_window_width, game_window_height))

clock = pygame.time.Clock()
running = True
grid.generate_grid(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid.give_me_tile()


    grid.draw_grid(screen)
    grid.highlight_current_tile(screen)
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()