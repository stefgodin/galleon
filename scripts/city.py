import pygame
import scripts.game_state as gs
import scripts.fake_grid as grid
import scripts.entity as en

def add_city(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    city = en.Entity()
    city.type = en.EntityType.CITY
    city.current_tile = -1
    city.hp = 8
    city.max_hp = 8
    city.team = 0
    city.attack_speed = 1000
    city.last_shot_t = 0
    game.entities.append(city)
    return idx

def draw_cities_ui(game: gs.GameState, screen: pygame.Surface):
    for city in game.entities:
        if city.type != en.EntityType.CITY:
            continue

        # Health bar
        [x, y] = grid.index_to_global_coord(game, city.current_tile)
        y -= game.fake_grid_tile_size/2
        health_bar_width = 10 * city.max_hp
        pygame.draw.rect(surface= screen, color= 'black', rect= [x - (health_bar_width/2) - 2, y - 16, health_bar_width + 4, 14])
        pygame.draw.rect(surface= screen, color= 'red', rect= [x - (health_bar_width/2), y - 14, 10 * city.hp, 10])

        if game.show_boxes:
            neihbors = grid.neighbor_tiles(game, city.current_tile, False)
            for tile in neihbors:
                [x, y] = grid.index_to_global_coord(game, tile)
                s = game.fake_grid_tile_size
                pygame.draw.lines(screen, pygame.Color(255, 0, 0), True, [
                    (x - s/2, y - s/2),
                    (x + s/2, y - s/2),
                    (x + s/2, y + s/2),
                    (x - s/2, y + s/2),
                ])