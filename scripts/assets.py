import os
import pygame
import scripts.game_state as gs

class Assets:
    TILE_CITY = "CITY_template.png"
    TILE_COVE = "COVE_template.png"
    TILE_ISLAND = "ISLAND_template.png"
    TILE_LAND = "LAND_template.png"
    TILE_SEA = "SEA_template.png"
    TILE_VOID = "VOID_template.png"
    TILE_CHOSEN = "CHOSEN_template.png"
    BOAT_BASE = "boat.png"
    MAIN_FONT = "_main_font"

def load_assets(game: gs.GameState):
    load_img(game, Assets.BOAT_BASE)
    load_img(game, Assets.TILE_CITY)
    load_img(game, Assets.TILE_COVE)
    load_img(game, Assets.TILE_ISLAND)
    load_img(game, Assets.TILE_LAND)
    load_img(game, Assets.TILE_SEA)
    load_img(game, Assets.TILE_VOID)
    load_img(game, Assets.TILE_CHOSEN)
    game.assets[Assets.MAIN_FONT] = pygame.font.SysFont("Arial", 30)
        
def load_img(game: gs.GameState, path: str):
    game.assets[path] = pygame.image.load(os.path.join(gs.ROOT_DIR,"assets",path)).convert_alpha()