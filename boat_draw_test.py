import pygame
from scripts.boat import add_boat,load_boat_assets,move_boats_to_destinations,draw_boats
from scripts.fake_grid import setup_grid,coord_to_index,draw_grid
from scripts.game_state import GameState

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    game = GameState()
    
    load_boat_assets(game)
    setup_grid(game)
    boat_1 = add_boat(game)

    while running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                game.mouse_pos.x = mouse_pos[0]
                game.mouse_pos.y = mouse_pos[1]
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = pygame.mouse.get_pressed()
                game.mouse_left = mouse_pressed[0]
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                game.key_1 = keys[pygame.K_1]
        
        # Update
        game.show_boxes = game.key_1

        if game.mouse_left:
            game.boats_destination[boat_1] = game.mouse_pos.copy()

        move_boats_to_destinations(game)

        # Render
        screen.fill("white")

        draw_grid(game, screen)
        draw_boats(game, screen)

        pygame.display.flip()

        game.dt = clock.tick(60)

    pygame.quit()

run()