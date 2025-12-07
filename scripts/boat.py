import os
import pygame
import scripts.game_state as gs
import scripts.fake_grid as grid

class BoatImg:
    BASE = 0

def setup_boats(game: gs.GameState):
    base_img = pygame.image.load(os.path.join(gs.ROOT_DIR,"assets","boat.png")).convert_alpha()
    base_img = pygame.transform.scale(base_img, (game.boat_base_size, game.boat_base_size))
    game.boat_imgs.append(base_img) # 0


def add_boat(game: gs.GameState) -> int:
    idx = game.boats_rect.__len__()
    boat_rect = pygame.Rect(0, 0, game.boat_base_size, game.boat_base_size)
    game.boats_rect.append(boat_rect)
    game.boats_current_tile.append(None)
    game.boats_img_idx.append(BoatImg.BASE)
    game.boats_destination_tile.append(-1)
    game.boats_path.append([])
    game.boats_final_tile.append(-1)
    game.boats_direction.append(pygame.Vector2(0, 0))
    game.boats_speed.append(1)
    return idx

def move_along_path(game: gs.GameState):
    move_to_dest(game)

def move_to_dest(game: gs.GameState):
    for i, boat_dest_tile in enumerate(game.boats_destination_tile):
        if boat_dest_tile == -1 and game.boats_path[i].__len__():
            game.boats_destination_tile[i] = game.boats_path[i].pop(0)

        boat_dest = grid.index_to_global_coord(game, boat_dest_tile) 
        if boat_dest == None:
            continue

        movement = game.boat_speed_const * game.boats_speed[i] * game.dt

        x_done = False
        left_x = boat_dest[0] - game.boats_rect[i].x - (game.boats_rect[i].w/2)
        game.boats_direction[i].x = 1 if left_x >= 0 else -1
        mov_x = movement * game.boats_direction[i].x
        if abs(left_x) <= abs(mov_x):
            game.boats_rect[i].x = boat_dest[0] - (game.boats_rect[i].w / 2)
            x_done = True
        else:
            game.boats_rect[i].x += mov_x

        y_done = False
        left_y = boat_dest[1] - game.boats_rect[i].y - (game.boats_rect[i].h/2)
        game.boats_direction[i].y = 1 if left_y >= 0 else -1
        mov_y = movement * game.boats_direction[i].y
        if abs(left_y) <= abs(mov_y):
            game.boats_rect[i].y = boat_dest[1] - (game.boats_rect[i].h / 2)
            y_done = True
        else:
            game.boats_rect[i].y += mov_y

        if x_done and y_done:
            game.boats_current_tile[i] = game.boats_destination_tile[i]
            game.boats_destination_tile[i] = -1

def draw_boats(game: gs.GameState, screen: pygame.Surface):
    for i, boat_rect in enumerate(game.boats_rect):
        boat_img = game.boat_imgs[game.boats_img_idx[i]]
        if game.boats_direction[i].x == 1:
            boat_img = pygame.transform.flip(boat_img, True, False)

        screen.blit(boat_img, boat_rect)

    if game.show_boxes:
        for boat_rect in game.boats_rect:
            pygame.draw.lines(screen, pygame.Color(255, 0, 0), True, [
                (boat_rect.x, boat_rect.y),
                (boat_rect.x + boat_rect.w, boat_rect.y),
                (boat_rect.x + boat_rect.w, boat_rect.y + boat_rect.h),
                (boat_rect.x, boat_rect.y + boat_rect.h),
            ])
