import os
import pygame
from .game_state import GameState,ROOT_DIR

class BoatImg:
    BASE = 0

def load_boat_assets(game: GameState):
    base_img = pygame.image.load(os.path.join(ROOT_DIR,"assets","boat.png")).convert_alpha()
    base_img = pygame.transform.scale(base_img, (game.boat_base_size, game.boat_base_size))
    game.boat_imgs.append(base_img) # 0


def add_boat(game: GameState) -> int:
    idx = game.boats_rect.__len__()
    boat_rect = pygame.Rect(0, 0, game.boat_base_size, game.boat_base_size)
    game.boats_rect.append(boat_rect)
    game.boats_img_idx.append(BoatImg.BASE)
    game.boats_destination.append(None)
    game.boats_direction.append(pygame.Vector2(0, 0))
    game.boats_speed.append(1)
    return idx

def move_boats_to_destinations(game: GameState) -> int:
    for i, boat_going_to in enumerate(game.boats_destination):
        if boat_going_to == None:
            continue

        movement = game.boat_speed_const * game.boats_speed[i] * game.dt

        x_done = False
        left_x = boat_going_to.x - game.boats_rect[i].x - (game.boats_rect[i].w/2)
        game.boats_direction[i].x = 1 if left_x >= 0 else -1
        mov_x = movement * game.boats_direction[i].x
        if abs(left_x) <= abs(mov_x):
            game.boats_rect[i].x = boat_going_to.x - (game.boats_rect[i].w / 2)
            x_done = True
        else:
            game.boats_rect[i].x += mov_x

        y_done = False
        left_y = boat_going_to.y - game.boats_rect[i].y - (game.boats_rect[i].h/2)
        game.boats_direction[i].y = 1 if left_y >= 0 else -1
        mov_y = movement * game.boats_direction[i].y
        if abs(left_y) <= abs(mov_y):
            game.boats_rect[i].y = boat_going_to.y - (game.boats_rect[i].h / 2)
            y_done = True
        else:
            game.boats_rect[i].y += mov_y

        if x_done and y_done:
            game.boats_destination[i] = None

def draw_boats(game: GameState, screen: pygame.Surface):
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