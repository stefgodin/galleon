import pygame
import math
import scripts.tile as hex_tile


pygame.init()
SIZE = 20

def flat_hex_corner( center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return pygame.Vector2(center.x + size * math.cos(angle_rad),\
                          center.y + size * math.sin(angle_rad) )

def draw_tile(tile):
    number_of_corners = len(tile.corners)
    for i in range(number_of_corners):        
        if i != (number_of_corners - 1):
            next_corner_index = i + 1
        else:
            next_corner_index = 0
            
        pygame.draw.line(screen, line_color, tile.corners[i], tile.corners[next_corner_index], 1)

game_window_width, game_window_height = [1280,720]
 
line_color = pygame.Color(0,0,0)

screen = pygame.display.set_mode((game_window_width, game_window_height))

map_colums = screen.get_width() / SIZE
map_rows = screen.get_height() / (math.sqrt(3) * SIZE /2)

clock = pygame.time.Clock()
running = True

screen.fill("white")

for c in range(int(map_colums+1)):
    for r in range(int(map_rows+1)):
        if (c + r) % 2 == 0:
            tile_coordinates = pygame.Vector2()
            tile_coordinates.xy = c, r
            tile = hex_tile.Tile(tile_coordinates)
            for corner_number in range(6):
                corner = flat_hex_corner(tile.display_coordinates, SIZE, corner_number)
                tile.add_corner(corner)
            draw_tile(tile)


# draw_tile(tile)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()