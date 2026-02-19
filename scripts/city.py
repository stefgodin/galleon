import pygame
import scripts.game_state as gs
import scripts.fake_grid as grid

class City:
    tile: int = -1
    hp: int = 8
    max_hp: int = 8
    team: int = 0
    level: int = 1
    attack_speed: int = 1000
    last_shot_at: int = 0

def add_city(game: gs.GameState) -> int:
    idx = game.cities.__len__()
    city = City()
    city.tile = -1
    city.hp = 8
    city.max_hp = 8
    city.team = 0
    city.level = 1
    city.attack_speed = 1000
    city.last_shot_at = 0
    game.cities.append(city)
    return idx

def draw_cities_ui(game: gs.GameState, screen: pygame.Surface):
    for city in game.cities:
        # Health bar
        [x, y] = grid.index_to_global_coord(game, city.tile)
        y -= game.fake_grid_tile_size/2
        health_bar_width = 10 * city.max_hp
        pygame.draw.rect(surface= screen, color= 'black', rect= [x - (health_bar_width/2) - 2, y - 16, health_bar_width + 4, 14])
        pygame.draw.rect(surface= screen, color= 'red', rect= [x - (health_bar_width/2), y - 14, 10 * city.hp, 10])

        if game.show_boxes:
            neihbors = grid.neighbor_tiles(game, city.tile, False)
            for tile in neihbors:
                [x, y] = grid.index_to_global_coord(game, tile)
                s = game.fake_grid_tile_size
                pygame.draw.lines(screen, pygame.Color(255, 0, 0), True, [
                    (x - s/2, y - s/2),
                    (x + s/2, y - s/2),
                    (x + s/2, y + s/2),
                    (x - s/2, y + s/2),
                ])