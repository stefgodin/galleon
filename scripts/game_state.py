import pygame
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

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
    boats_rect: list[pygame.Rect] = []
    boats_img_idx: list[pygame.Surface] = []
    boats_destination: list[tuple[int, int]|None] = []
    boats_path: list[list[int]|None] = []
    boats_final_tile: list[int] = []
    boats_direction: list[pygame.Vector2] = []
    boats_speed: list[int] = []
