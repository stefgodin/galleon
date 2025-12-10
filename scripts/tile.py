import math
import pygame

class Tile:
    # doubled-height hexagon pattern
    tile_horizontal_spacing = 3/2 * 20
    tile_vertical_spacing = math.sqrt(3) * 20

    def __init__(self, coordinates):
        self.corners = []
        self.coordinates = coordinates
        self.display_coordinates = pygame.Vector2(coordinates.x * self.tile_horizontal_spacing, coordinates.y * self.tile_vertical_spacing / 2)
    
    def add_corner(self, corner):
        self.corners.append(corner)