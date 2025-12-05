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

def coord_to_index(game: GameState, x, y):
    return game.fake_grid_x * y + x

def global_coord_to_grid_index(game: GameState, gx, gy):
    return

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