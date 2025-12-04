import os
import pygame
from .game_state import GameState,ROOT_DIR

def load_boat_assets(game: GameState):
    game.boat_base_img = pygame.image.load(os.path.join(ROOT_DIR,"assets","boat.png")).convert_alpha()

def add_boat(game: GameState) -> int:
    idx = game.boat_rect.__len__()
    boat_rect = pygame.Rect(0,0,256,256)
    game.boat_rect.append(boat_rect)
    game.boat_img.append(pygame.transform.scale(game.boat_base_img, (boat_rect.w, boat_rect.h)))
    game.boat_going_to.append(None)
    game.boat_direction.append(pygame.Vector2(0, 0))
    game.boat_speed.append(1)
    return idx