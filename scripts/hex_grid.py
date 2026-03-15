import math
import pygame
import random
from enum import Enum
import scripts.game_state as gs
from scripts.tile import TILE_COLORS, TileType,Tile

SIZE = 20
line_color = pygame.Color(0,0,0)
highlight_line_color = pygame.Color(240,240,240)
tile_horizontal_spacing = 3/2 * SIZE
tile_vertical_spacing = math.sqrt(3) * SIZE



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

def draw_tile_for_asset_generation(screen: pygame.Surface, tile_coords: tuple[int, int], tile_type: TileType):
    corners = hex_corners(pygame.Vector2(tile_coords[0], tile_coords[1]))
    print(tile_type.value)
    pygame.draw.polygon(screen, pygame.Color(TILE_COLORS[tile_type.value]), corners, 0)
    pygame.draw.polygon(screen, pygame.Color(0, 0, 0), corners, 1)


def hex_coords_to_screen_coords(grid_postion: tuple[int, int]) -> tuple[int, int]: 
    return (grid_postion[0] * tile_horizontal_spacing, grid_postion[1] * tile_vertical_spacing / 2)

def draw_grid(game_state: gs.GameState ,screen: pygame.Surface):
    for tile in game_state.hex_grid_tiles:
        tile_coords = hex_coords_to_screen_coords(tile.hex_coords)
        draw_tile(game_state, screen, tile)

def highlight_current_tile(screen):
    mouse_pos = pygame.mouse.get_pos()
    mouse_y = 2 * mouse_pos[1] / tile_vertical_spacing
    x = round(mouse_pos[0] / tile_horizontal_spacing)
    y = round(2 * mouse_pos[1] / tile_vertical_spacing)
    z = 6
    if (x + y) % 2 != 0:
        if mouse_y > y:
            y += 1
        else:
            y -= 1
    hex_coords = hex_coords_to_screen_coords(pygame.Vector3(x,y,z))
    draw_tile_for_asset_generation(screen, hex_coords, highlight_line_color)

def give_me_tile():
    mouse_pos = pygame.mouse.get_pos()
    mouse_y = 2 * mouse_pos[1] / tile_vertical_spacing
    x = round(mouse_pos[0] / tile_horizontal_spacing)
    y = round(2 * mouse_pos[1] / tile_vertical_spacing)
    if (x + y) % 2 != 0:
        if mouse_y > y:
            y += 1
        else:
            y -= 1
    z = 6
    print(x, y)

def draw_tile(game: gs.GameState, render_target: pygame.Surface, tile: Tile):
    tile_coords = hex_coords_to_screen_coords(tile.hex_coords)
    tile_img = game.assets[tile.sprite_id]
    render_target.blit(tile_img, tile_coords)

def generate_grid(game_state: gs.GameState):
    map_colums = game_state.screen_width / SIZE
    map_rows = game_state.screen_height / (math.sqrt(3) * SIZE /2)

    for c in range(int(map_colums+1)):
        for r in range(int(map_rows+1)):
            if (c + r) % 2 == 0:
                tile_type = random.choice(list(TileType))
                Tile.add_tile(game_state, (c, r), tile_type)

def generate_grid_tile_image():
    surface = pygame.Surface(((2*SIZE+2),(2*SIZE+2)))
    surface.fill((255, 255, 255))
    for tile_type in TileType:
        tile = pygame.Vector2(SIZE, SIZE)
        draw_tile_for_asset_generation(surface, tile, tile_type)
        file_name = tile_type.name + "_template.png"
        pygame.image.save(surface, file_name)


