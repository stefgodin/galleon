import pygame
from .game_state import GameState
import random

class GridTiles:
    VOID = 0
    SEA = 1
    LAND = 2

def setup_grid(game: GameState):
    for _ in range(0, game.fake_grid_x * game.fake_grid_y):
        game.fake_grid_tiles.append(GridTiles.SEA if random.random() > 0.2 else GridTiles.LAND)

def global_to_grid_coord(game: GameState, x: float, y: float) -> tuple[int, int]|None:
    if x < 0 or x >= (game.fake_grid_x * game.fake_grid_tile_size) or y < 0 or y >= (game.fake_grid_y * game.fake_grid_tile_size):
        return None

    return (
        (int)(x / game.fake_grid_tile_size),
        (int)(y / game.fake_grid_tile_size)
    )

def grid_to_global_coord(game: GameState, x: int, y: int) -> tuple[float, float]|None:
    if x < 0 or x >= game.fake_grid_x or y < 0 or y >= game.fake_grid_y:
        return None

    return ((x * game.fake_grid_tile_size) + game.fake_grid_tile_size/2, (y * game.fake_grid_tile_size) + game.fake_grid_tile_size/2)

def coord_to_index(game: GameState, x: int, y: int) -> int:
    if x < 0 or x >= game.fake_grid_x or y < 0 or y >= game.fake_grid_y:
        return -1

    return game.fake_grid_x * y + x

def index_to_coord(game: GameState, idx: int) -> tuple[int, int]|None:
    if idx < 0 or idx >= game.fake_grid_tiles.__len__():
        return None
    
    return (idx % game.fake_grid_x, (int)(idx / game.fake_grid_x))


def draw_grid(game: GameState, surface: pygame.Surface):
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

def path_find(game: GameState):
    for i, final_tile in enumerate(game.boats_final_tile):
        if final_tile == -1:
            continue
        
        