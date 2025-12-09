import scripts.game_state as gs
import scripts.fake_grid as grid

def find_closest_path_tiles(game: gs.GameState, tile: int, not_moveable_tiles: list[int] = []) -> list[int]:
    if tile == -1:
        return []
    
    if grid.is_path_tile(game, tile):
        return [tile]
    
    to_check: list[int] = [tile]
    checked: list[int] = []
    tiles: list[int] = []
    while not tiles.__len__() and to_check.__len__():
        next_check_batch = []
        while to_check.__len__():
            tile = to_check.pop()
            if tile in checked:
                continue

            checked.append(tile)
            if grid.is_path_tile(game, tile) and tile not in not_moveable_tiles:
                tiles.append(tile)
            else:
                next_check_batch += grid.neighbor_tiles(game, tile, False)
        
        to_check = next_check_batch
    
    return tiles


# A*
def find_path(game: gs.GameState, from_tile: int, to_tile: int, ignore_tiles: list[int] = []) -> list[int]:
    if from_tile == -1:
        return []
    
    potential_to_tiles = find_closest_path_tiles(game, to_tile, ignore_tiles)
    if not potential_to_tiles.__len__():
        return []
    else:
        min_dist = -1
        for tile in potential_to_tiles:
            dist = grid.calc_dist(game, from_tile, tile)
            if min_dist == -1 or min_dist > dist:
                min_dist = dist
                to_tile = tile

    opened: list[int] = [from_tile]

    # g_scores is distance from start node to target node
    g_scores: dict[int, int] = {}
    g_scores[from_tile] = 0

    # f_scores is estimated distance from target node to end node
    f_scores: dict[int, int] = {}
    f_scores[from_tile] = grid.calc_dist(game, from_tile, to_tile)

    came_from: dict[int, int] = {}

    while opened.__len__():
        current = opened.pop(0)
        if current == to_tile:
            break # Done

        for neighbor in grid.neighbor_tiles(game, current, True):
            if neighbor in ignore_tiles:
                continue

            neighbor_g_score = g_scores[current] + grid.calc_dist(game, current, neighbor)
            if neighbor in g_scores and neighbor_g_score >= g_scores[neighbor]:
                continue
                
            came_from[neighbor] = current
            g_scores[neighbor] = neighbor_g_score
            f_scores[neighbor] = neighbor_g_score + grid.calc_dist(game, neighbor, to_tile)
            
            if neighbor not in opened:
                opened.append(neighbor)

        opened.sort(key=lambda idx: f_scores[idx]) # sort by f

    # reconstruct path from
    if to_tile not in came_from:
        return []
    
    path = []
    current = to_tile
    while current != from_tile:
        path.append(current) # will not append the last tile, by design (it's the start)
        current = came_from[current]

    path.reverse()
    return path
    