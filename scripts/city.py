import scripts.game_state as gs
import scripts.entity as en

def add_city(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    city = en.Entity()
    city.type = en.EntityType.CITY
    city.current_tile = -1

    city.can_fight = True
    city.hp = 8
    city.max_hp = 8
    city.team = 0
    city.attack_speed = 1000
    city.last_shot_t = 0

    game.entities.append(city)
    return idx