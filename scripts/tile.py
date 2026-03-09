from enum import Enum
import scripts.game_state as gs
import pygame

colors = [(0, 0, 0), (0, 255, 255), (243, 206, 57), (131, 131, 131), (76, 0, 153), (0, 152, 0), (150, 152, 150)]

class TileType(Enum):
    VOID = 0
    SEA = 1
    ISLAND = 2
    CITY = 3
    COVE = 4
    LAND = 5
    CHOSEN = 6

class Tile:
    type: TileType = TileType.VOID
    hex_coords: tuple[int, int] = (0, 0)
    sprite : pygame.Surface|None = None

    def add_tile(game : gs.GameState, hex_coords: tuple[int, int], tile_type: TileType) -> int:
        idx = len(game.hex_grid_tiles)
        tile = Tile()
        tile.hex_coords = hex_coords
        tile.type = tile_type
        game.hex_grid_tiles.append(tile)
        return idx
    
    def get_sprite(self) -> pygame.Surface:
        sprite = pygame.image.load(self.type.name + "_template.png")
        

