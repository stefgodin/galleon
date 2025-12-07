import pygame
import scripts.boat as boat
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.find_path as pf

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    game = gs.GameState()
    
    boat.setup_boats(game)
    grid.setup_grid(game)
    boat_1 = boat.add_boat(game)
    game.boats_current_tile[boat_1] = 0
    game.boats_rect[boat_1].center = grid.index_to_global_coord(game, game.boats_current_tile[boat_1])

    while running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                game.mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = pygame.mouse.get_pressed()
                game.mouse_left = mouse_pressed[0]
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                game.key_1 = keys[pygame.K_1]
        
        # Update
        game.show_boxes = game.key_1

        if game.mouse_pos is not None:
            if game.mouse_left:
                final_tile = grid.global_coord_to_index(game, game.mouse_pos[0], game.mouse_pos[1])
                game.boats_path[boat_1] = pf.find_path(game, game.boats_current_tile[boat_1], final_tile)

            grid_coord = grid.global_to_grid_coord(game, game.mouse_pos[0], game.mouse_pos[1])
            if grid_coord is not None:
                game.fake_grid_hovered_tile = grid.coord_to_index(game, grid_coord[0], grid_coord[1])
            else:
                game.fake_grid_hovered_tile = -1

        boat.move_along_path(game)

        # Render
        screen.fill("white")

        grid.draw_grid(game, screen)
        boat.draw_boats(game, screen)

        pygame.display.flip()

        game.dt = clock.tick(60)

    pygame.quit()

run()