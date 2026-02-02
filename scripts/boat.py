import os
import pygame
import scripts.game_state as gs
import scripts.fake_grid as grid
import scripts.find_path as pf

class BoatImg:
    BASE = 0

def setup_boats(game: gs.GameState):
    base_img = pygame.image.load(os.path.join(gs.ROOT_DIR,"assets","boat.png")).convert_alpha()
    base_img = pygame.transform.scale(base_img, (game.boat_base_size, game.boat_base_size))
    game.boat_imgs.append(base_img) # 0


def add_boat(game: gs.GameState) -> int:
    idx = game.boats.__len__()
    boat_rect = pygame.Rect(0, 0, game.boat_base_size, game.boat_base_size)
    boat = gs.Boat()
    boat.rect = boat_rect
    boat.current_tile = None
    boat.img_idx = BoatImg.BASE
    boat.destination_tile = -1
    boat.path = []
    boat.direction = pygame.Vector2(0, 0)
    boat.speed = 1
    game.boats.append(boat)
    return idx

def move_along_path(game: gs.GameState):
    move_to_dest(game)

def move_to_dest(game: gs.GameState):
    for boat in game.boats:
        if boat.destination_tile == -1 and boat.path.__len__():
            if next((other_boat for other_boat in game.boats if other_boat.current_tile == boat.path[0]), False):
                # TODO: also check for surrounding occupied boat tiles, not just the one we're trying to access
                boat.path = pf.find_path(game, boat.current_tile, boat.path[-1], [boat.path[0]]) 
                continue

            boat.destination_tile = boat.path.pop(0)
            boat.current_tile = boat.destination_tile # Hum?

        boat_dest_xy = grid.index_to_global_coord(game, boat.destination_tile) 
        if boat_dest_xy == None:
            continue

        movement = game.boat_speed_const * boat.speed * game.dt

        x_done = False
        left_x = boat_dest_xy[0] - boat.rect.x - (boat.rect.w/2)
        boat.direction.x = 1 if left_x >= 0 else -1
        mov_x = movement * boat.direction.x
        if abs(left_x) <= abs(mov_x):
            boat.rect.x = boat_dest_xy[0] - (boat.rect.w / 2)
            x_done = True
        else:
            boat.rect.x += mov_x

        y_done = False
        left_y = boat_dest_xy[1] - boat.rect.y - (boat.rect.h/2)
        boat.direction.y = 1 if left_y >= 0 else -1
        mov_y = movement * boat.direction.y
        if abs(left_y) <= abs(mov_y):
            boat.rect.y = boat_dest_xy[1] - (boat.rect.h / 2)
            y_done = True
        else:
            boat.rect.y += mov_y

        if x_done and y_done:
            boat.destination_tile = -1

def draw_boats(game: gs.GameState, screen: pygame.Surface):
    for boat in game.boats:
        boat_img = game.boat_imgs[boat.img_idx]
        if boat.direction.x == 1:
            boat_img = pygame.transform.flip(boat_img, True, False)

        screen.blit(boat_img, boat.rect)

        if game.show_boxes:
            pygame.draw.lines(screen, pygame.Color(255, 0, 0), True, [
                (boat.rect.x, boat.rect.y),
                (boat.rect.x + boat.rect.w, boat.rect.y),
                (boat.rect.x + boat.rect.w, boat.rect.y + boat.rect.h),
                (boat.rect.x, boat.rect.y + boat.rect.h),
            ])
