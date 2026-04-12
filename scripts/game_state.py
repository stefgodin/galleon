import pygame
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scripts.tile import Tile
    from scripts.entity import Entity
    from scripts.entity_upgrade import Upgrade
    from scripts.team import Team
    from scripts.ui import UIState

ROOT_DIR = Path(__file__).resolve().parent.parent

class GameState:
    should_close: bool = False
    screen_width: int = 1280
    screen_height: int = 720
    ui: 'UIState' = None

    mouse_pos: tuple[int, int]|None = None
    mouse_left: bool = False
    mouse_right: bool = False
    key_1: bool = False
    key_tab: bool = False
    key_u: bool = False

    player_team: int = -1

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

    hex_grid_tiles: list['Tile'] = []

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
    upgrades: list['Upgrade'] = []

    # Players and team
    teams: list['Team'] = []


