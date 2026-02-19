import pygame
import random
import scripts.boat as b
import scripts.city as c
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
    
    b.setup_boats(game)
    grid.setup_grid(game)
    for idx in range(0, 2):
        i = b.add_boat(game)
        boat = game.boats[i]
        boat.current_tile = random.randint(0, game.fake_grid_tiles.__len__() - 1)
        boat.rect.center = grid.index_to_global_coord(game, boat.current_tile)
        boat.team = 1 if idx == 0 else 2
    
    for _ in range(0, 5):
        i = c.add_city(game)
        city = game.cities[i]
        city.tile = random.randint(0, game.fake_grid_tiles.__len__() - 1)
        game.fake_grid_tiles[city.tile] = grid.GridTiles.CITY

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

        for boat in game.boats:
            if boat.team == 1 or boat.path.__len__():
               continue 
            
            tile = random.randint(0, game.fake_grid_tiles.__len__() - 1)
            boat.path = pf.find_path(game, boat.current_tile, tile)

        for boat in game.boats:
            if boat.hp <= 0 or boat.last_shot_at + boat.attack_speed > game.tt:
                continue

            can_attack = []
            attackable_tiles = grid.neighbor_tiles(game, boat.current_tile, False)
            for other_boat in game.boats:
                if other_boat.hp <= 0 or other_boat == boat or other_boat.team == boat.team:
                    continue

                if other_boat.current_tile in attackable_tiles:
                    can_attack.append(other_boat)
            
            for city in game.cities:
                if city.hp <= 0 or city.team == boat.team:
                    continue
                
                if city.tile in attackable_tiles:
                    can_attack.append(city)

            if can_attack.__len__():
                attack_target = can_attack[random.randint(0, can_attack.__len__() - 1)]
                if isinstance(attack_target, b.Boat):
                    attack_target.hp -= 1
                elif isinstance(attack_target, c.City):
                    attack_target.hp -= 1
                
                boat.last_shot_at = game.tt

        for city in game.cities:
            if city.hp <= 0 or city.last_shot_at + city.attack_speed > game.tt:
                continue

            can_attack = []
            attackable_tiles = grid.neighbor_tiles(game, city.tile, False)
            for boat in game.boats:
                if boat.hp <= 0 or boat.team == city.team:
                    continue

                if boat.current_tile in attackable_tiles:
                    can_attack.append(boat)
            
            for other_city in game.cities:
                if other_city.hp <= 0 or other_city == city or other_city.team == city.team:
                    continue
                
                if other_city.tile in attackable_tiles:
                    can_attack.append(other_city)

            if can_attack.__len__():
                attack_target = can_attack[random.randint(0, can_attack.__len__() - 1)]
                if isinstance(attack_target, b.Boat):
                    attack_target.hp -= 1
                    pass
                elif isinstance(attack_target, c.City):
                    attack_target.hp -= 1
                
                city.last_shot_at = game.tt
                

        if game.mouse_pos is not None:
            if game.mouse_left:
                final_tile = grid.global_coord_to_index(game, game.mouse_pos[0], game.mouse_pos[1])
                for boat in game.boats: 
                    if boat.team == 1:
                        boat.path = pf.find_path(game, boat.current_tile, final_tile)

            grid_coord = grid.global_to_grid_coord(game, game.mouse_pos[0], game.mouse_pos[1])
            if grid_coord is not None:
                game.fake_grid_hovered_tile = grid.coord_to_index(game, grid_coord[0], grid_coord[1])
            else:
                game.fake_grid_hovered_tile = -1

        b.move_along_path(game)

        # Render
        screen.fill("white")

        grid.draw_grid(game, screen)
        b.draw_boats(game, screen)
        c.draw_cities_ui(game, screen)
        b.draw_boats_ui(game, screen)

        pygame.display.flip()

        game.dt = clock.tick(120)
        game.tt += game.dt
        pygame.display.set_caption("Galleon (" + str(clock.get_fps()) + " fps)")

    pygame.quit()

run()