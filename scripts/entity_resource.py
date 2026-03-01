import scripts.game_state as gs
import random

class Resources:
    GOLD = 0
    RHUM = 1
    WOOD = 2

def spread_resource_yield(game_state: gs.GameState):
    resource_slot_count = 0
    for entity in game_state.entities:
        if entity.can_yield_resources:
            resource_slot_count += 2
    
    even_split_count = int(resource_slot_count/3) 
    resource_count = {
        Resources.GOLD: even_split_count,
        Resources.RHUM: even_split_count,
        Resources.WOOD: even_split_count,
    }

    while resource_count[Resources.GOLD] or resource_count[Resources.RHUM] or resource_count[Resources.WOOD]:
        choices = list(filter(lambda r: resource_count[r], resource_count.keys()))
        res = random.choice(choices) 
        resource_count[res] -= 1

        attributed = False
        for entity in game_state.entities:
            if entity.can_yield_resources and entity.resource_a == -1:
                entity.resource_a = res
                attributed = True
                break
        
        if attributed:
            continue

        for entity in game_state.entities:
            if entity.can_yield_resources and entity.resource_b == -1:
                entity.resource_b = res 
                break


def tick_yield(game_state: gs.GameState):
    for entity in game_state.entities:
        if not entity.can_yield_resources:
            continue

        if entity.defeated:
            continue

        entity.resource_yield_timer = min(entity.resource_yield_timer + 1, entity.max_resource_yield_timer)
        if entity.resource_yield_timer == entity.max_resource_yield_timer:
            entity.resource_yield_timer = 0
            team = game_state.teams[entity.team]
            for resource in [entity.resource_a, entity.resource_b]:
                match resource:
                    case Resources.GOLD:
                        team.gold += 1
                    case Resources.RHUM:
                        team.rhum += 1
                    case Resources.WOOD:
                        team.wood += 1
