import pygame
from pathlib import Path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.entity import Entity
    from scripts.team import Team

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
    tick_diff_t: int = 0 #ms
    tick_rate: int = 25

    # Fake grid
    fake_grid_x: int = 20
    fake_grid_y: int = 10
    fake_grid_tile_size: int = 64 # Todo move to grid
    fake_grid_tiles: list[int] = []
    fake_grid_hovered_tile: int = -1

    # Win condition
    max_game_timer: int = 0
    game_timer: int = 0
    real_time_max_game_timer: int = 0 # in s
    winner_team: int = -1
    game_over: bool = False

    # Entities
    entities: list['Entity'] = []
    show_boxes: bool = False
    assets: dict[str, pygame.Surface|pygame.font.Font] = {}
    boat_base_size: int = 48

    # Players and team
    teams: list['Team'] = []

