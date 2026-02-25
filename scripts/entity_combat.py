import random
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.entity as en

def tick_combat(game_state: gs.GameState):
    for entity in game_state.entities:
        if not entity.can_fight:
            continue
        
        if entity.defeated or entity.last_shot_t + (entity.attack_speed * game_state.tick_rate) > game_state.game_t:
            continue

        atk_target_list: list[en.Entity] = []
        atk_tiles = grid.neighbor_tiles(game_state, entity.current_tile)
        for other_entity in game_state.entities:
            if not entity.can_fight:
                continue

            if other_entity == entity or other_entity.defeated or other_entity.team == entity.team:
                continue

            if other_entity.current_tile in atk_tiles:
                atk_target_list.append(other_entity)
        
        if atk_target_list.__len__():
            atk_target = atk_target_list[random.randint(0, atk_target_list.__len__() - 1)]
            atk_target.hp = max(atk_target.hp - 1, 0)
            if atk_target.hp == 0:
                atk_target.defeated = True
                if atk_target.can_be_captured:
                    atk_target.capture_timer = 0
           
            entity.last_shot_t = game_state.game_t

def tick_capture(game_state: gs.GameState):
    for entity in game_state.entities:
        if not entity.can_be_captured or not entity.defeated:
            continue

        neighbors = grid.neighbor_tiles(game_state, entity.current_tile)

        capturing_team = -1
        for other_entity in game_state.entities:
            if not other_entity.can_capture or other_entity.defeated or not other_entity.current_tile in neighbors:
                continue 

            entity.capture_contested = capturing_team != -1 and capturing_team != other_entity.team
            capturing_team = capturing_team if capturing_team != -1 else other_entity.team

        if entity.capture_contested:
            continue
        
        if entity.capture_timer > 0 and (entity.capture_team == -1 or entity.capture_team != capturing_team):
            entity.capture_timer = max(0, entity.capture_timer - 1)
        elif capturing_team != -1:
            entity.capture_team = capturing_team
            entity.capture_timer = min(entity.capture_timer + 1, entity.max_capture_timer)
        
        if entity.capture_timer == entity.max_capture_timer:
            entity.capture_timer = 0
            entity.team = entity.capture_team
            entity.hp = entity.max_hp
            entity.defeated = False