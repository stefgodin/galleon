import pygame
from scripts.boat import Boats,load_boat_assets,IMG_BOAT

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    asset = load_boat_assets()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        boats = Boats()
        boat_1 = boats.add_boat()

        screen.fill("white")

        boat_pos = boats.screen_pos[boat_1]
        boat_rect = asset[IMG_BOAT].get_rect()
        boat_rect.topleft = boat_pos

        screen.blit(asset[IMG_BOAT], boat_rect)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

run()