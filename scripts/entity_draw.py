import pygame
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.entity as en

class DRAW_LAYERS:
    ENTITY = 0
    ENTITY_UI = 1

def draw_entities(game: gs.GameState, render_target: pygame.Surface):
    for layer in range(DRAW_LAYERS.ENTITY, DRAW_LAYERS.ENTITY_UI + 1):
        for entity in game.entities:
            match entity.type:
                case en.EntityType.BOAT:
                    draw_boat(game, render_target, entity, layer)
                case en.EntityType.CITY:
                    draw_city(game, render_target, entity, layer)
                case en.EntityType.COVE:
                    draw_cove(game, render_target, entity, layer)


def draw_boat(game: gs.GameState, render_target: pygame.Surface, boat: en.Entity, layer: int):
    team_color = game.teams[boat.team].color
    if layer == DRAW_LAYERS.ENTITY:
        boat_img = game.assets[boat.sprite_id]
        boat_img = pygame.transform.scale(boat_img, (game.boat_base_size, game.boat_base_size))
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
        if game.show_boxes:
            neihbors = grid.neighbor_tiles(game, boat.current_tile)
            for tile in neihbors:
                [x, y] = grid.index_to_global_coord(game, tile)
                s = game.fake_grid_tile_size
                pygame.draw.lines(render_target, team_color, True, [
                    (x - s/2, y - s/2),
                    (x + s/2, y - s/2),
                    (x + s/2, y + s/2),
                    (x - s/2, y + s/2),
                ])


def draw_city(game: gs.GameState, render_target: pygame.Surface, city: en.Entity, layer: int):
    team_color = game.teams[city.team].color
    [x, y] = grid.index_to_global_coord(game, city.current_tile)
    if layer == DRAW_LAYERS.ENTITY:
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - game.fake_grid_tile_size/2, y - game.fake_grid_tile_size/2, game.fake_grid_tile_size, game.fake_grid_tile_size])
    elif layer == DRAW_LAYERS.ENTITY_UI:
        if not city.defeated:
            # Health bar
            hp_bar_y = y - game.fake_grid_tile_size/2
            health_bar_w = 10 * city.max_hp
            pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (health_bar_w/2) - 2, hp_bar_y - 16, health_bar_w + 4, 14])
            pygame.draw.rect(surface= render_target, color= 'black', rect= [x - (health_bar_w/2), hp_bar_y - 14, health_bar_w, 10])
            pygame.draw.rect(surface= render_target, color= 'red', rect= [x - (health_bar_w/2), hp_bar_y - 14, city.hp/city.max_hp * health_bar_w, 10])
        else:
            # Capture progress
            capture_team_color = game.teams[city.capture_team].color if city.capture_team != -1 and not city.capture_contested else game.teams[0].color
            capture_bar_y = y - game.fake_grid_tile_size/2
            capture_timer_w = 10 * city.max_hp 
            pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (capture_timer_w/2) - 2, capture_bar_y - 16, capture_timer_w + 4, 14])
            pygame.draw.rect(surface= render_target, color= 'black', rect= [x - (capture_timer_w/2), capture_bar_y - 14, capture_timer_w, 10])
            pygame.draw.rect(surface= render_target, color= capture_team_color, rect= [x - (capture_timer_w/2), capture_bar_y - 14, city.capture_timer/city.max_capture_timer*capture_timer_w, 10])
        
        # Resource yield
        if city.resource_a != -1 and game.teams[city.team].can_win:
            y -= game.fake_grid_tile_size/2
            resource_timer_w = 10 * city.max_hp
            pygame.draw.rect(surface= render_target, color= 'black', rect= [x - (resource_timer_w/2), y, city.resource_yield_timer/city.max_resource_yield_timer * resource_timer_w, 4])

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

def draw_cove(game: gs.GameState, render_target: pygame.Surface, cove: en.Entity, layer: int):
    team_color = game.teams[cove.team].color
    [x, y] = grid.index_to_global_coord(game, cove.current_tile)
    if layer == DRAW_LAYERS.ENTITY:
        pygame.draw.rect(surface= render_target, color= 'black', rect= [x - game.fake_grid_tile_size/2, y - game.fake_grid_tile_size/2, game.fake_grid_tile_size, game.fake_grid_tile_size])
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - game.fake_grid_tile_size/2 + 3, y - game.fake_grid_tile_size/2 + 3, game.fake_grid_tile_size - 6, game.fake_grid_tile_size - 6])