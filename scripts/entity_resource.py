import scripts.game_state as gs

class Resources:
    GOLD = 0
    RHUM = 1
    WOOD = 2

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