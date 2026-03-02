import pygame
import random
from scripts.game_runner import GameRunner
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.assets as ast
import scripts.entity_move as en_move
import scripts.entity_combat as en_combat
import scripts.entity_draw as en_draw
import scripts.entity_resource as en_res
import scripts.entity_upgrade as en_upg
import scripts.entity as en
import scripts.win_condition as wc
import scripts.team as t

class WinTest(GameRunner):
    # Called once at the start of the game
    @staticmethod
    def init(game_state: gs.GameState):
        ast.load_assets(game_state)
        grid.setup_grid(game_state)
        wc.setup_win_condition(game_state)
        en_upg.setup_upgrades(game_state)
        t.setup_teams(game_state, 2)
        game_state.player_team = next((t for t in game_state.teams if t.can_win)).id
        
        for team in game_state.teams:
            if not team.can_win:
                continue

            i = en.add_cove(game_state)
            cove = game_state.entities[i]
            cove.current_tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
            game_state.fake_grid_tiles[cove.current_tile] = grid.GridTiles.LAND
            cove.team = team.id

            for _ in range(0, 2):
                i = en.add_boat(game_state)
                boat = game_state.entities[i]
                boat.current_tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
                boat.sprite_rect.center = grid.index_to_global_coord(game_state, boat.current_tile)
                boat.team = team.id
        
        for _ in range(0, 5):
            i = en.add_city(game_state)
            city = game_state.entities[i]
            city.current_tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
            game_state.fake_grid_tiles[city.current_tile] = grid.GridTiles.LAND
        
        en_res.spread_resource_yield(game_state)

    # Called on every input event
    @staticmethod
    def input(game_state: gs.GameState, evt: pygame.event.Event):
        if evt.type == pygame.MOUSEMOTION:
            game_state.mouse_pos = pygame.mouse.get_pos()
        elif evt.type == pygame.MOUSEBUTTONDOWN or evt.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = pygame.mouse.get_pressed()
            game_state.mouse_left = mouse_pressed[0]
            game_state.mouse_right = mouse_pressed[2]
        elif evt.type == pygame.KEYDOWN or evt.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            game_state.key_1 = keys[pygame.K_1]
            game_state.key_tab = keys[pygame.K_TAB]
            if keys[pygame.K_KP_PLUS]:
                game_state.tick_rate = max(1, game_state.tick_rate - 1)
            elif keys[pygame.K_KP_MINUS]:
                game_state.tick_rate = game_state.tick_rate + 1
            elif keys[pygame.K_KP_ENTER]:
                game_state.tick_rate = 25


    # Called every fixed tick based on tick_rate (simulation speed), is not tied to framerate
    @staticmethod
    def tick(game_state: gs.GameState):
        if game_state.game_over:
            return

        en_move.tick_movement(game_state)
        en_combat.tick_combat(game_state)
        en_combat.tick_capture(game_state)
        en_combat.tick_respawn(game_state)
        en_res.tick_yield(game_state)
        wc.tick_win_condition(game_state)
    
    # Called once per frame for real-time updates (or interpolation)
    @staticmethod
    def update(game_state: gs.GameState):
        if game_state.game_over:
            return

        game_state.show_boxes = game_state.key_1

        for entity in game_state.entities:
            if not entity.can_move or entity.team == game_state.player_team or entity.path.__len__():
               continue 
            
            # Automatically controlling entities movements that are not in team 1
            tile = random.randint(0, game_state.fake_grid_tiles.__len__() - 1)
            en_move.change_entity_path(game_state, entity, tile)


        if game_state.mouse_pos is not None:
            mouse_tile = grid.global_coord_to_index(game_state, game_state.mouse_pos[0], game_state.mouse_pos[1])

            if game_state.mouse_left:
                for entity in game_state.entities: 
                    if entity.can_move and entity.team == game_state.player_team:
                        en_move.change_entity_path(game_state, entity, mouse_tile)
            
            if game_state.mouse_right:
                for entity in game_state.entities:
                    entity.show_upgrades = entity.current_tile == mouse_tile

            game_state.fake_grid_hovered_tile = mouse_tile
        
        en_move.update_movement_view(game_state)
    
    # Called once per frame to redraw
    @staticmethod
    def render(game_state: gs.GameState, render_target: pygame.Surface):
        grid.draw_grid(game_state, render_target)
        en_draw.draw_entities(game_state, render_target)
        wc.draw_game_timer(game_state, render_target)
        if game_state.game_over:
            wc.draw_game_over(game_state, render_target)
        elif game_state.key_tab:
            t.draw_team_info(game_state, render_target)

WinTest().run()