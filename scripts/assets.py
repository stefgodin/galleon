import os
import pygame
import scripts.game_state as gs

class Assets:
    BOAT_BASE = "boat.png"

def load_assets(game: gs.GameState):
    load_img(game, Assets.BOAT_BASE)

def load_img(game: gs.GameState, path: str):
    game.assets[path] = pygame.image.load(os.path.join(gs.ROOT_DIR,"assets",path)).convert_alpha()