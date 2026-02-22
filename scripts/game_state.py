import pygame
from pathlib import Path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.city import City
    from scripts.boat import Boat

ROOT_DIR = Path(__file__).resolve().parent.parent

class GameState:
    should_close = False
    screen_width: int = 1280
    screen_height: int = 720

    mouse_pos: tuple[int, int]|None = None
    mouse_left: bool = False
    key_1: bool = False

    game_t: int = 0 #ms
    delta_t: int = 0 #ms
    tick_t: int = 0 #ms
    tick_rate: int = 50

    # Fake grid
    fake_grid_border_thickness = 2
    fake_grid_x = 20
    fake_grid_y = 10
    fake_grid_tile_size = 64
    fake_grid_tiles: list[int] = []
    fake_grid_hovered_tile: int = -1

    # Boats
    show_boxes: bool = False
    boat_imgs: list[pygame.Surface] = []
    boat_speed_const: int = 0.1
    boat_base_size: int = 48
    boats: list['Boat'] = []

    # Cities
    cities: list['City'] = []
