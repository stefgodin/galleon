import scripts.fake_grid as grid
import scripts.find_path as pf
import scripts.game_state as gs
import scripts.entity as en

def change_entity_path(game: gs.GameState, entity: en.Entity, destination_tile: int, ignore_tiles = []):
    if destination_tile == -1:
        entity.path = []
    else:
        current_tile = entity.current_tile if entity.next_tile == -1 else entity.next_tile
        entity.path = pf.find_path(game, current_tile, destination_tile, ignore_tiles) 


def update_movement(game: gs.GameState):
    for entity in game.entities:
        if not entity.can_move:
            continue
        
        if entity.next_tile == -1 and entity.path.__len__():
            if not next((other_entity for other_entity in game.entities if entity.can_move and (other_entity.current_tile == entity.path[0] or other_entity.next_tile == entity.path[0])), False):
                entity.prev_tile = entity.current_tile
                entity.next_tile = entity.path.pop(0)
                entity.next_tile_dist = 1.0
                # TODO: also check for surrounding occupied boat tiles, not just the one we're trying to access
                # change_entity_path(game, entity, entity.path[-1], [entity.path[0]])
                # continue

        
        if entity.next_tile == -1:
            continue
        
        progress_dist = game.delta_t / game.tick_rate / entity.speed
        entity.next_tile_dist = max(0, entity.next_tile_dist - progress_dist)

        prev_xy = grid.index_to_coord(game, entity.prev_tile)
        next_xy = grid.index_to_coord(game, entity.next_tile) 
        x_diff = next_xy[0] - prev_xy[0]
        y_diff = next_xy[1] - prev_xy[1]
        entity.direction.x = x_diff if x_diff else entity.direction.x
        entity.direction.y = y_diff if y_diff else entity.direction.y

        prev_global_xy = grid.index_to_global_coord(game, entity.prev_tile)
        x = prev_global_xy[0] + ((1 - entity.next_tile_dist) * game.fake_grid_tile_size * x_diff)
        y = prev_global_xy[1] + ((1 - entity.next_tile_dist) * game.fake_grid_tile_size * y_diff)

        entity.sprite_rect.center = (x, y)

        if entity.next_tile_dist <= 0.5:
            entity.current_tile = entity.next_tile

        if entity.next_tile_dist == 0:
            entity.next_tile = -1