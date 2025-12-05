import pygame
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

class GameState:
    screen: pygame.Surface|None = None

    mouse_pos: pygame.Vector2 = pygame.Vector2()
    mouse_left: bool = False
    key_1: bool = False

    dt: int = 0 #ms

    # Assets

    # Fake grid
    fake_grid_border_thickness = 2
    fake_grid_x = 60
    fake_grid_y = 60
    fake_grid_tile_size = 64
    fake_grid_tiles: list[int] = []

    # Boats
    show_boxes: bool = False
    boat_imgs: list[pygame.Surface] = []
    boat_speed_const: int = 0.3
    boat_base_size: int = 48
    boats_rect: list[pygame.Rect] = []
    boats_img_idx: list[pygame.Surface] = []
    boats_destination: list[pygame.Vector2|None] = []
    boats_direction: list[pygame.Vector2] = []
    boats_speed: list[int] = []
