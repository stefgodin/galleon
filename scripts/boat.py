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

    boat.sprite_rect = boat_rect
    boat.sprite_id = ast.Assets.BOAT_BASE
    
    boat.can_move = True
    boat.current_tile = -1
    boat.current_tile_dist = -1
    boat.destination_tile = -1
    boat.path = []
    boat.direction = pygame.Vector2(0, 0)
    boat.speed = 1

    boat.can_fight = True
    boat.team =  0
    boat.hp =  10
    boat.max_hp =  10
    boat.attack_speed =  1000
    boat.last_shot_t =  0

    game.entities.append(boat)
    return idx

def draw_boats(game: gs.GameState, screen: pygame.Surface):
    for boat in game.entities:
        if boat.type != en.EntityType.BOAT:
            continue

        boat_img = game.assets[boat.sprite_id]
        boat_img = pygame.transform.scale(boat_img, (game.boat_base_size, game.boat_base_size))
        if boat.direction.x == 1:
            boat_img = pygame.transform.flip(boat_img, True, False)

        screen.blit(boat_img, boat.sprite_rect)

def draw_boats_ui(game: gs.GameState, screen: pygame.Surface):
    for boat in game.entities:
        if boat.type != en.EntityType.BOAT:
            continue

        # Health bar
        [x, y] = boat.sprite_rect.midtop
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