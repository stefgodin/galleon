import pygame
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

class GameState:
    mouse_pos: pygame.Vector2 = pygame.Vector2()
    mouse_left: bool = False
    key_1: bool = False

    dt: int = 0 #ms

    # Assets
    boat_base_img: pygame.Surface|None = None

    # Boats
    show_boxes: bool = False
    boat_speed_const: int = 0.3
    boat_rect: list[pygame.Rect] = []
    boat_img: list[pygame.Surface] = []
    boat_going_to: list[pygame.Vector2|None] = []
    boat_direction: list[pygame.Vector2] = []
    boat_speed: list[int] = []
