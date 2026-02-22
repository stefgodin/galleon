import random
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.entity as en

def update_combat(game_state: gs.GameState):
    for entity in game_state.entities:
        if not entity.can_fight:
            continue
        
        if entity.hp <= 0 or entity.last_shot_t + entity.attack_speed > game_state.game_t:
            continue

        atk_target_list: list[en.Entity] = []
        atk_tiles = grid.neighbor_tiles(game_state, entity.current_tile, False)
        for other_entity in game_state.entities:
            if not entity.can_fight:
                continue

            if other_entity == entity or other_entity.hp <= 0 or other_entity.team == entity.team:
                continue

            if other_entity.current_tile in atk_tiles:
                atk_target_list.append(other_entity)
        
        if atk_target_list.__len__():
            atk_target = atk_target_list[random.randint(0, atk_target_list.__len__() - 1)]
            atk_target.hp = max(atk_target.hp - 1, 0)
            
            entity.last_shot_t = game_state.game_t