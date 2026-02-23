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