import pygame
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.entity as en

class DRAW_LAYERS:
    ENTITY = 0
    ENTITY_UI = 1

TEAM_COLORS = [
    "#607D8B",
    "#4CAF50",
    "#F44336",
    "#2196F3",
    "#FFEB3B",
    "#FF9800",
    "#00BCD4",
    "#673AB7",
]

def draw_entities(game_state: gs.GameState, render_target: pygame.Surface):
    for layer in range(DRAW_LAYERS.ENTITY, DRAW_LAYERS.ENTITY_UI + 1):
        for entity in game_state.entities:
            match entity.type:
                case en.EntityType.BOAT:
                    draw_boat(game_state, render_target, entity, layer)
                case en.EntityType.CITY:
                    draw_city(game_state, render_target, entity, layer)


def draw_boat(game_state: gs.GameState, render_target: pygame.Surface, boat: en.Entity, layer: int):
    team_color = TEAM_COLORS[boat.team % TEAM_COLORS.__len__()]
    if layer == DRAW_LAYERS.ENTITY:
        boat_img = game_state.assets[boat.sprite_id]
        boat_img = pygame.transform.scale(boat_img, (game_state.boat_base_size, game_state.boat_base_size))
        if boat.direction.x == 1:
            boat_img = pygame.transform.flip(boat_img, True, False)

        render_target.blit(boat_img, boat.sprite_rect)
    elif layer == DRAW_LAYERS.ENTITY_UI:
        # Health bar
        [x, y] = boat.sprite_rect.midtop
        health_bar_width = 10 * boat.max_hp
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (health_bar_width/2) - 2, y - 12, health_bar_width + 4, 14])
        pygame.draw.rect(surface= render_target, color= 'black', rect= [x - (health_bar_width/2), y - 10, health_bar_width, 10])
        pygame.draw.rect(surface= render_target, color= 'red', rect= [x - (health_bar_width/2), y - 10, 10 * boat.hp, 10])

        # Boxes
        if game_state.show_boxes:
            neihbors = grid.neighbor_tiles(game_state, boat.current_tile)
            for tile in neihbors:
                [x, y] = grid.index_to_global_coord(game_state, tile)
                s = game_state.fake_grid_tile_size
                pygame.draw.lines(render_target, team_color, True, [
                    (x - s/2, y - s/2),
                    (x + s/2, y - s/2),
                    (x + s/2, y + s/2),
                    (x - s/2, y + s/2),
                ])


def draw_city(game: gs.GameState, render_target: pygame.Surface, city: en.Entity, layer: int):
    team_color = TEAM_COLORS[city.team % TEAM_COLORS.__len__()]
    [x, y] = grid.index_to_global_coord(game, city.current_tile)
    if layer == DRAW_LAYERS.ENTITY:
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - game.fake_grid_tile_size/2, y - game.fake_grid_tile_size/2, game.fake_grid_tile_size, game.fake_grid_tile_size])
    elif layer == DRAW_LAYERS.ENTITY_UI:
        # Health bar
        y -= game.fake_grid_tile_size/2
        health_bar_width = 10 * city.max_hp
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (health_bar_width/2) - 2, y - 16, health_bar_width + 4, 14])
        pygame.draw.rect(surface= render_target, color= 'black', rect= [x - (health_bar_width/2), y - 14, health_bar_width, 10])
        pygame.draw.rect(surface= render_target, color= 'red', rect= [x - (health_bar_width/2), y - 14, 10 * city.hp, 10])

        # Boxes
        if game.show_boxes:
            neihbors = grid.neighbor_tiles(game, city.current_tile)
            for tile in neihbors:
                [x, y] = grid.index_to_global_coord(game, tile)
                s = game.fake_grid_tile_size
                pygame.draw.lines(render_target, team_color, True, [
                    (x - s/2, y - s/2),
                    (x + s/2, y - s/2),
                    (x + s/2, y + s/2),
                    (x - s/2, y + s/2),
                ])