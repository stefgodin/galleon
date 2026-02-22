import os
import pygame
import scripts.fake_grid as grid
import scripts.find_path as pf
import scripts.game_state as gs
import scripts.entity as en
import scripts.assets as ast

def add_boat(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    boat_rect = pygame.Rect(0, 0, game.boat_base_size, game.boat_base_size)
    boat = en.Entity()
    boat.type = en.EntityType.BOAT
    boat.can_fight = True
    boat.can_move = True
    boat.rect = boat_rect
    boat.current_tile = None
    boat.sprite_id = ast.Assets.BOAT_BASE
    boat.destination_tile = -1
    boat.path = []
    boat.direction = pygame.Vector2(0, 0)
    boat.speed = 1
    boat.team =  0
    boat.hp =  10
    boat.max_hp =  10
    boat.attack_speed =  1000
    boat.last_shot_t =  0

    game.entities.append(boat)
    return idx

def move_to_dest(game: gs.GameState):
    for entity in game.entities:
        if not entity.can_move:
            continue
        
        if entity.destination_tile == -1 and entity.path.__len__():
            if next((other_entity for other_entity in game.entities if entity.can_move and other_entity.current_tile == entity.path[0]), False):
                # TODO: also check for surrounding occupied boat tiles, not just the one we're trying to access
                entity.path = pf.find_path(game, entity.current_tile, entity.path[-1], [entity.path[0]]) 
                continue

            entity.destination_tile = entity.path.pop(0)
            entity.current_tile = entity.destination_tile # Hum?

        boat_dest_xy = grid.index_to_global_coord(game, entity.destination_tile) 
        if boat_dest_xy == None:
            continue

        movement = game.boat_speed_const * entity.speed * game.delta_t

        x_done = False
        left_x = boat_dest_xy[0] - entity.rect.x - (entity.rect.w/2)
        entity.direction.x = 1 if left_x >= 0 else -1
        mov_x = movement * entity.direction.x
        if abs(left_x) <= abs(mov_x):
            entity.rect.x = boat_dest_xy[0] - (entity.rect.w / 2)
            x_done = True
        else:
            entity.rect.x += mov_x

        y_done = False
        left_y = boat_dest_xy[1] - entity.rect.y - (entity.rect.h/2)
        entity.direction.y = 1 if left_y >= 0 else -1
        mov_y = movement * entity.direction.y
        if abs(left_y) <= abs(mov_y):
            entity.rect.y = boat_dest_xy[1] - (entity.rect.h / 2)
            y_done = True
        else:
            entity.rect.y += mov_y

        if x_done and y_done:
            entity.destination_tile = -1

def draw_boats(game: gs.GameState, screen: pygame.Surface):
    for boat in game.entities:
        if boat.type != en.EntityType.BOAT:
            continue

        boat_img = game.assets[boat.sprite_id]
        boat_img = pygame.transform.scale(boat_img, (game.boat_base_size, game.boat_base_size))
        if boat.direction.x == 1:
            boat_img = pygame.transform.flip(boat_img, True, False)

        screen.blit(boat_img, boat.rect)

def draw_boats_ui(game: gs.GameState, screen: pygame.Surface):
    for boat in game.entities:
        if boat.type != en.EntityType.BOAT:
            continue

        # Health bar
        [x, y] = boat.rect.midtop
        health_bar_width = 10 * boat.max_hp
        pygame.draw.rect(surface= screen, color= 'black', rect= [x - (health_bar_width/2) - 2, y - 12, health_bar_width + 4, 14])
        pygame.draw.rect(surface= screen, color= 'red', rect= [x - (health_bar_width/2), y - 10, 10 * boat.hp, 10])


        if game.show_boxes:
            neihbors = grid.neighbor_tiles(game, boat.current_tile, False)
            for tile in neihbors:
                [x, y] = grid.index_to_global_coord(game, tile)
                s = game.fake_grid_tile_size
                pygame.draw.lines(screen, pygame.Color(255, 0, 0), True, [
                    (x - s/2, y - s/2),
                    (x + s/2, y - s/2),
                    (x + s/2, y + s/2),
                    (x - s/2, y + s/2),
                ])