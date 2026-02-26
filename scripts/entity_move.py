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


def tick_movement(game: gs.GameState):
    for entity in game.entities:
        if not entity.can_move or entity.defeated:
            continue
        
        if entity.next_tile == -1 and entity.path.__len__():
            next_path_blocked = False
            for other_entity in game.entities:
                if other_entity.intangible:
                    continue

                if other_entity.current_tile != entity.path[0] and other_entity.next_tile != entity.path[0]:
                    continue

                next_path_blocked = True
            
            if not next_path_blocked:
                entity.prev_tile = entity.current_tile
                entity.next_tile = entity.path.pop(0)
                entity.next_tile_dist = 1.0
                # TODO: also check for surrounding occupied boat tiles, not just the one we're trying to access
                # change_entity_path(game, entity, entity.path[-1], [entity.path[0]])
                # continue

        
        if entity.next_tile == -1:
            continue
        
        entity.next_tile_dist = max(0, ((entity.next_tile_dist * entity.speed) - 1) / entity.speed )

        prev_xy = grid.index_to_coord(game, entity.prev_tile)
        next_xy = grid.index_to_coord(game, entity.next_tile) 
        x_diff = next_xy[0] - prev_xy[0]
        y_diff = next_xy[1] - prev_xy[1]
        entity.direction.x = x_diff if x_diff else entity.direction.x
        entity.direction.y = y_diff if y_diff else entity.direction.y

        if entity.next_tile_dist <= 0.5:
            entity.current_tile = entity.next_tile

        if entity.next_tile_dist == 0:
            entity.next_tile = -1

def update_movement_view(game: gs.GameState):
    for entity in game.entities:
        if not entity.can_move or entity.defeated:
            continue

        if entity.next_tile == -1:
            entity.sprite_rect.center = grid.index_to_global_coord(game, entity.current_tile)
            continue
        
        view_next_tile_dist = max(0, ((entity.next_tile_dist * entity.speed) - (game.tick_diff_t / game.tick_rate)) / entity.speed )

        prev_xy = grid.index_to_coord(game, entity.prev_tile)
        next_xy = grid.index_to_coord(game, entity.next_tile) 
        x_diff = next_xy[0] - prev_xy[0]
        y_diff = next_xy[1] - prev_xy[1]

        prev_global_xy = grid.index_to_global_coord(game, entity.prev_tile)
        x = prev_global_xy[0] + ((1 - view_next_tile_dist) * game.fake_grid_tile_size * x_diff)
        y = prev_global_xy[1] + ((1 - view_next_tile_dist) * game.fake_grid_tile_size * y_diff)

        entity.sprite_rect.center = (x, y)