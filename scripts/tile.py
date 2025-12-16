import math
import pygame
import random

class Tile:
    # doubled-height hexagon pattern
    tile_horizontal_spacing = 3/2 * 40
    tile_vertical_spacing = math.sqrt(3) * 40
    tile_types = [('sea',(0,255,255)),
                 ('island',(243,206,57)),
                 ('city',(131,131,131)),
                 ('cove',(76,0,153)),
                 ('land', (0, 152, 0))]

    def __init__(self, coordinates):
        self.corners = []
        self.coordinates = coordinates
        self.display_coordinates = pygame.Vector2(coordinates.x * self.tile_horizontal_spacing, coordinates.y * self.tile_vertical_spacing / 2)
        self.type = self.tile_types[random.randint(0,(len(self.tile_types)-1))]
    
    def add_corner(self, corner):
        self.corners.append(corner)