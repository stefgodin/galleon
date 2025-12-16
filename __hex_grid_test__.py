import pygame
import math
import scripts.tile as hex_tile


pygame.init()

game_window_width, game_window_height = [1280,720]

screen = pygame.display.set_mode((game_window_width, game_window_height))

clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()