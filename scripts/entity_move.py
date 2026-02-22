import scripts.fake_grid as grid
import scripts.find_path as pf
import scripts.game_state as gs

def update_movement(game: gs.GameState):
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

        dest_xy = grid.index_to_global_coord(game, entity.destination_tile) 
        if dest_xy == None:
            continue

        movement = game.speed_const * entity.speed * game.delta_t

        x_done = False
        left_x = dest_xy[0] - entity.sprite_rect.x - (entity.sprite_rect.w/2)
        entity.direction.x = 1 if left_x >= 0 else -1
        mov_x = movement * entity.direction.x
        if abs(left_x) <= abs(mov_x):
            entity.sprite_rect.x = dest_xy[0] - (entity.sprite_rect.w / 2)
            x_done = True
        else:
            entity.sprite_rect.x += mov_x

        y_done = False
        left_y = dest_xy[1] - entity.sprite_rect.y - (entity.sprite_rect.h/2)
        entity.direction.y = 1 if left_y >= 0 else -1
        mov_y = movement * entity.direction.y
        if abs(left_y) <= abs(mov_y):
            entity.sprite_rect.y = dest_xy[1] - (entity.sprite_rect.h / 2)
            y_done = True
        else:
            entity.sprite_rect.y += mov_y

        if x_done and y_done:
            entity.destination_tile = -1