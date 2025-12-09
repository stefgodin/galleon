import pygame
import random
import scripts.boat as boat
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.find_path as pf

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Galleon")
    clock = pygame.time.Clock()
    running = True

    game = gs.GameState()
    
    boat.setup_boats(game)
    grid.setup_grid(game)
    for _ in range(0, 10):
        id = boat.add_boat(game)
        game.boats_current_tile[id] = random.randint(0, game.fake_grid_tiles.__len__() - 1)
        game.boats_rect[id].center = grid.index_to_global_coord(game, game.boats_current_tile[id])

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

        for i, path in enumerate(game.boats_path):
            if path.__len__():
               continue 
            
            tile = random.randint(0, game.fake_grid_tiles.__len__() - 1)
            game.boats_path[i] = pf.find_path(game, game.boats_current_tile[i], tile)


        if game.mouse_pos is not None:
            if game.mouse_left:
                final_tile = grid.global_coord_to_index(game, game.mouse_pos[0], game.mouse_pos[1])
                for i, current_tile in enumerate(game.boats_current_tile): 
                    game.boats_path[i] = pf.find_path(game, current_tile, final_tile)

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

        game.dt = clock.tick(120)
        pygame.display.set_caption("Galleon (" + str(clock.get_fps()) + " fps)")

    pygame.quit()

run()