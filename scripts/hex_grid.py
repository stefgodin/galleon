import math
import pygame
import random
from enum import Enum

SIZE = 20
line_color = pygame.Color(0,0,0)
grid = []
tile_horizontal_spacing = 3/2 * SIZE
tile_vertical_spacing = math.sqrt(3) * SIZE
colors = [(0, 0, 0), (0, 255, 255), (243, 206, 57), (131, 131, 131), (76, 0, 153), (0, 152, 0)]

class Tile(Enum):
    VOID = 0,
    SEA = 1,
    ISLAND = 2,
    CITY = 3
    COVE = 4
    LAND = 5

def flat_hex_corner(center, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return pygame.Vector2(center.x + SIZE * math.cos(angle_rad),\
                          center.y + SIZE * math.sin(angle_rad) )

def hex_corners(tile_center_coords):
    number_of_corners = 6
    corners = []

    for i in range(number_of_corners):
        corners.append(flat_hex_corner(tile_center_coords, i))

    return corners

def draw_tile(screen, tile_coords):
    tile_corners = hex_corners(tile_coords)

    pygame.draw.polygon(screen, colors[int(tile_coords.z)],tile_corners)
    for i in range(len(tile_corners)):   
        if i != (len(tile_corners) - 1):
            next_corner_index = i + 1
        else:
            next_corner_index = 0
            
        pygame.draw.line(screen, line_color, tile_corners[i], tile_corners[next_corner_index], 3)

def position_to_coords(grid_postion: pygame.Vector3):
    return pygame.Vector3(grid_postion.x * tile_horizontal_spacing, grid_postion.y * tile_vertical_spacing / 2, grid_postion.z)

def draw_grid(screen):
    for tile in grid:
        tile_coords = position_to_coords(tile)
        draw_tile(screen, tile_coords)

def generate_grid(screen):
    map_colums = screen.get_width() / SIZE
    map_rows = screen.get_height() / (math.sqrt(3) * SIZE /2)
    
    screen.fill("white")

    for c in range(int(map_colums+1)):
        for r in range(int(map_rows+1)):
            if (c + r) % 2 == 0:
                color = random.randint(1, 5)
                tile_info = pygame.Vector3()
                tile_info.xyz = c, r, color 
                grid.append(tile_info)
