import os
import pygame
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
IMG_BOAT = "boat"

class Boats:
    screen_pos: list[pygame.Vector2] = []
    active: list[bool] = [] 

    def add_boat(self) -> int:
        self.screen_pos.append(pygame.Vector2(x=0,y=0))
        self.active.append(True)
        return self.active.__len__() - 1 

def load_boat_assets() -> dict[str, pygame.Surface]:
    return {
        IMG_BOAT:  pygame.image.load(os.path.join(ROOT_DIR,"assets","boat.png")).convert_alpha()
    }