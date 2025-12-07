import pygame
import scripts.game_state as gs
import random

class GridTiles:
    VOID = 0
    SEA = 1
    LAND = 2

def setup_grid(game: gs.GameState):
    for _ in range(0, game.fake_grid_x * game.fake_grid_y):
        game.fake_grid_tiles.append(GridTiles.SEA if random.random() > 0.2 else GridTiles.LAND)

def global_to_grid_coord(game: gs.GameState, x: float, y: float) -> tuple[int, int]|None:
    if x < 0 or x >= (game.fake_grid_x * game.fake_grid_tile_size) or y < 0 or y >= (game.fake_grid_y * game.fake_grid_tile_size):
        return None

    return (
        (int)(x / game.fake_grid_tile_size),
        (int)(y / game.fake_grid_tile_size)
    )

def global_coord_to_index(game: gs.GameState, x: float, y: float) -> int:
    xy = global_to_grid_coord(game, x, y)
    if xy is None:
        return -1
    
    return coord_to_index(game, xy[0], xy[1])

def grid_to_global_coord(game: gs.GameState, x: int, y: int) -> tuple[float, float]|None:
    if x < 0 or x >= game.fake_grid_x or y < 0 or y >= game.fake_grid_y:
        return None

    return ((x * game.fake_grid_tile_size) + game.fake_grid_tile_size/2, (y * game.fake_grid_tile_size) + game.fake_grid_tile_size/2)

def coord_to_index(game: gs.GameState, x: int, y: int) -> int:
    if x < 0 or x >= game.fake_grid_x or y < 0 or y >= game.fake_grid_y:
        return -1

    return game.fake_grid_x * y + x

def index_to_coord(game: gs.GameState, idx: int) -> tuple[int, int]|None:
    if idx < 0 or idx >= game.fake_grid_tiles.__len__():
        return None
    
    return (idx % game.fake_grid_x, (int)(idx / game.fake_grid_x))

def index_to_global_coord(game: gs.GameState, idx: int) -> tuple[int, int]|None:
    coord = index_to_coord(game, idx)
    if coord is None:
        return None
    
    return grid_to_global_coord(game, coord[0], coord[1])

def calc_dist(game: gs.GameState, from_tile: int, to_tile: int) -> int:
    xy_from = index_to_coord(game, from_tile)
    if xy_from is None:
        return -1

    xy_to = index_to_coord(game, to_tile)
    if xy_to is None:
        return -1
    
    return abs(xy_to[0] - xy_from[0]) + abs(xy_to[1] - xy_from[1])

def is_path_tile(game: gs.GameState, tile: int) -> bool:
    return game.fake_grid_tiles[tile] == GridTiles.SEA

def neighbor_tiles(game: gs.GameState, idx: int, path_only: bool) -> list[int]:
    neighbors = []
    xy = index_to_coord(game, idx)
    if xy is None:
        return neighbors
    
    (x, y) = xy
    neighbors = [
        coord_to_index(game, x, y - 1),
        coord_to_index(game, x - 1, y), 
        coord_to_index(game, x, y + 1),
        coord_to_index(game, x + 1, y),
    ] 
    return [n for n in neighbors if n > -1 and (not path_only or is_path_tile(game, n))]

def draw_grid(game: gs.GameState, surface: pygame.Surface):
    colors = {
        GridTiles.VOID: "black",
        GridTiles.SEA: pygame.Color(60, 160, 240),
        GridTiles.LAND: pygame.Color(240, 240, 30),
    }
    for y in range(0, game.fake_grid_y):
        for x in range(0, game.fake_grid_x):
            tile_type = game.fake_grid_tiles[coord_to_index(game, x, y)]
            pygame.draw.rect(surface, colors[tile_type], [
                (x * game.fake_grid_tile_size, y * game.fake_grid_tile_size),
                (game.fake_grid_tile_size, game.fake_grid_tile_size)
            ])
    
    
    if game.fake_grid_hovered_tile > -1:
        (x, y) = index_to_coord(game, game.fake_grid_hovered_tile)
        pygame.draw.rect(surface, "black", [
            (x * game.fake_grid_tile_size, y * game.fake_grid_tile_size),
            (game.fake_grid_tile_size, game.fake_grid_tile_size)
        ], 3)
