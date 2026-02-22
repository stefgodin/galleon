import pygame
import random
import scripts.boat as b
import scripts.city as c
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.find_path as pf
from scripts.game_runner import GameRunner

class CombatTest(GameRunner):
    # Called once at the start of the game
    @staticmethod
    def init(game_state: gs.GameState):
        b.setup_boats(game_state)
        grid.setup_grid(game_state)
        for idx in range(0, 2):
            i = b.add_boat(game_state)
            boat = game_state.boats[i]
            boat.current_tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
            boat.rect.center = grid.index_to_global_coord(game_state, boat.current_tile)
            boat.team = 1 if idx == 0 else 2
        
        for _ in range(0, 5):
            i = c.add_city(game_state)
            city = game_state.cities[i]
            city.tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
            game_state.fake_grid_tiles[city.tile] = grid.GridTiles.CITY

    # Called on every input event
    @staticmethod
    def input(game_state: gs.GameState, evt: pygame.event.Event):
        if evt.type == pygame.MOUSEMOTION:
            game_state.mouse_pos = pygame.mouse.get_pos()
        elif evt.type == pygame.MOUSEBUTTONDOWN or evt.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = pygame.mouse.get_pressed()
            game_state.mouse_left = mouse_pressed[0]
        elif evt.type == pygame.KEYDOWN or evt.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            game_state.key_1 = keys[pygame.K_1]

    # Called every fixed tick based on tick_rate (simulation speed), is not tied to framerate
    @staticmethod
    def tick(game_state: gs.GameState):
        pass
    
    # Called once per frame for real-time updates (or interpolation)
    @staticmethod
    def update(game_state: gs.GameState):
        game_state.show_boxes = game_state.key_1

        for boat in game_state.boats:
            if boat.team == 1 or boat.path.__len__():
               continue 
            
            tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
            boat.path = pf.find_path(game_state, boat.current_tile, tile)

        for boat in game_state.boats:
            if boat.hp <= 0 or boat.last_shot_at + boat.attack_speed > game_state.game_t:
                continue

            can_attack = []
            attackable_tiles = grid.neighbor_tiles(game_state, boat.current_tile, False)
            for other_boat in game_state.boats:
                if other_boat.hp <= 0 or other_boat == boat or other_boat.team == boat.team:
                    continue

                if other_boat.current_tile in attackable_tiles:
                    can_attack.append(other_boat)
            
            for city in game_state.cities:
                if city.hp <= 0 or city.team == boat.team:
                    continue
                
                if city.tile in attackable_tiles:
                    can_attack.append(city)

            if can_attack.__len__():
                attack_target = can_attack[random.randint(0, can_attack.__len__() - 1)]
                if isinstance(attack_target, b.Boat):
                    attack_target.hp -= 1
                elif isinstance(attack_target, c.City):
                    attack_target.hp -= 1
                
                boat.last_shot_at = game_state.game_t

        for city in game_state.cities:
            if city.hp <= 0 or city.last_shot_at + city.attack_speed > game_state.game_t:
                continue

            can_attack = []
            attackable_tiles = grid.neighbor_tiles(game_state, city.tile, False)
            for boat in game_state.boats:
                if boat.hp <= 0 or boat.team == city.team:
                    continue

                if boat.current_tile in attackable_tiles:
                    can_attack.append(boat)
            
            for other_city in game_state.cities:
                if other_city.hp <= 0 or other_city == city or other_city.team == city.team:
                    continue
                
                if other_city.tile in attackable_tiles:
                    can_attack.append(other_city)

            if can_attack.__len__():
                attack_target = can_attack[random.randint(0, can_attack.__len__() - 1)]
                if isinstance(attack_target, b.Boat):
                    attack_target.hp -= 1
                    pass
                elif isinstance(attack_target, c.City):
                    attack_target.hp -= 1
                
                city.last_shot_at = game_state.game_t
                

        if game_state.mouse_pos is not None:
            if game_state.mouse_left:
                final_tile = grid.global_coord_to_index(game_state, game_state.mouse_pos[0], game_state.mouse_pos[1])
                for boat in game_state.boats: 
                    if boat.team == 1:
                        boat.path = pf.find_path(game_state, boat.current_tile, final_tile)

            grid_coord = grid.global_to_grid_coord(game_state, game_state.mouse_pos[0], game_state.mouse_pos[1])
            if grid_coord is not None:
                game_state.fake_grid_hovered_tile = grid.coord_to_index(game_state, grid_coord[0], grid_coord[1])
            else:
                game_state.fake_grid_hovered_tile = -1

        b.move_along_path(game_state)
    
    # Called once per frame to redraw
    @staticmethod
    def render(game_state: gs.GameState, render_target: pygame.Surface):
        grid.draw_grid(game_state, render_target)
        b.draw_boats(game_state, render_target)
        c.draw_cities_ui(game_state, render_target)
        b.draw_boats_ui(game_state, render_target)

CombatTest().run()