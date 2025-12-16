import math
import pygame
from enum import Enum

SIZE = 20
line_color = pygame.Color(0,0,0)
grid = []
tile_horizontal_spacing = 3/2 * 40
tile_vertical_spacing = math.sqrt(3) * 40

class Tile(Enum):
    VOID = 0,
    SEA = 1,
    ISLAND = 2,
    CITY = 3
    COVE = 4
    LAND = 5

def flat_hex_corner( center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return pygame.Vector2(center.x + size * math.cos(angle_rad),\
                          center.y + size * math.sin(angle_rad) )

def draw_tile(screen, tile_coords):
    number_of_corners = 6
    # pygame.draw.polygon(screen, 'Blue', tile.corners)
    for i in range(number_of_corners):   
        if i != (number_of_corners - 1):
            next_corner_index = i + 1
        else:
            next_corner_index = 0
            
        pygame.draw.line(screen, line_color, flat_hex_corner(tile_coords, SIZE, i), flat_hex_corner(tile_coords, SIZE, next_corner_index), 3)

def position_to_coords(grid_postion: pygame.Vector2):
    return pygame.Vector2(grid_postion.x * tile_horizontal_spacing, grid_postion.y * tile_vertical_spacing / 2)

def draw_grid(screen):
    map_colums = screen.get_width() / SIZE
    map_rows = screen.get_height() / (math.sqrt(3) * SIZE /2)
    
    screen.fill("white")

    for c in range(int(map_colums+1)):
        for r in range(int(map_rows+1)):
            if (c + r) % 2 == 0:
                tile_position = pygame.Vector2()
                tile_position.xy = c, r
                tile_coords = position_to_coords(tile_position)
                draw_tile(screen)
