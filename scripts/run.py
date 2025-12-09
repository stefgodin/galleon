import pygame
from scripts.game_state import GameState

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    game = GameState()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()