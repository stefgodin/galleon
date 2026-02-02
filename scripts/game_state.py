import pygame
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

class Boat:
    rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    current_tile: int = -1
    img_idx: pygame.Surface = -1
    destination_tile: int = -1
    path: list[int] = []
    direction: pygame.Vector2 = pygame.Vector2(0, 0)
    speed: int = 0


class GameState:
    screen: pygame.Surface|None = None

    mouse_pos: tuple[int, int]|None = None
    mouse_left: bool = False
    key_1: bool = False

    dt: int = 0 #ms

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
    boat_speed_const: int = 0.3
    boat_base_size: int = 48
    boats: list[Boat] = []
