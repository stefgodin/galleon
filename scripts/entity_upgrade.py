import pygame
import scripts.game_state as gs
import scripts.entity as en
import scripts.entity_resource as en_res

class Upgrade:
    id: int = -1
    entity_type: int = -1
    group: str = ""
    level: int = 1
    inc_hp: int = -1
    inc_attack: int = -1
    inc_speed: int = -1
    cost: dict[int, int] = {}

def setup_upgrades(game: gs.GameState):
    # TODO Upgrade cost could be randomized (resource-wise) to increase variability of gameplay

    # Boat attack upgrades
    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.BOAT
    upgrade.group = "attack"
    upgrade.level = 1
    upgrade.inc_attack = 13
    upgrade.cost = {
        en_res.Resources.RHUM: 3,
        en_res.Resources.WOOD: 3,
    }

    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.BOAT
    upgrade.group = "attack"
    upgrade.level = 2
    upgrade.inc_attack = 10
    upgrade.cost = {
        en_res.Resources.RHUM: 5,
        en_res.Resources.WOOD: 5,
    }

    # Boat hp upgrades
    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.BOAT
    upgrade.group = "hp"
    upgrade.level = 1
    upgrade.inc_hp = 15
    upgrade.cost = {
        en_res.Resources.GOLD: 3,
        en_res.Resources.WOOD: 3,
    }

    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.BOAT
    upgrade.group = "hp"
    upgrade.level = 2
    upgrade.inc_hp = 20
    upgrade.cost = {
        en_res.Resources.GOLD: 5,
        en_res.Resources.WOOD: 5,
    }

    # Boat speed upgrades
    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.BOAT
    upgrade.group = "speed"
    upgrade.level = 1
    upgrade.inc_speed = 16
    upgrade.cost = {
        en_res.Resources.GOLD: 3,
        en_res.Resources.RHUM: 3,
    }

    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.BOAT
    upgrade.group = "speed"
    upgrade.level = 2
    upgrade.inc_speed = 12
    upgrade.cost = {
        en_res.Resources.GOLD: 5,
        en_res.Resources.RHUM: 5,
    }

    # City upgrades
    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.CITY
    upgrade.group = "all"
    upgrade.level = 1
    upgrade.inc_hp = 15
    upgrade.inc_attack = 13
    upgrade.cost = {
        en_res.Resources.GOLD: 4,
        en_res.Resources.WOOD: 4,
    }

    i = add_upgrade(game)
    upgrade = game.upgrades[i]
    upgrade.entity_type = en.EntityType.CITY
    upgrade.group = "all"
    upgrade.level = 2
    upgrade.inc_hp = 20
    upgrade.inc_attack = 10
    upgrade.cost = {
        en_res.Resources.GOLD: 6,
        en_res.Resources.WOOD: 6,
    }


def add_upgrade(game: gs.GameState): 
    idx = game.upgrades.__len__()
    upgrade = Upgrade()
    upgrade.id = idx
    game.upgrades.append(upgrade)
    return idx

def can_upgrade(game: gs.GameState, entity: en.Entity, upgrade: Upgrade):
    if game.player_team != entity.team or entity.type != upgrade.entity_type or upgrade.id in entity.upgrades:
        return False
    
    for lower_upg in game.upgrades:
        if lower_upg.entity_type != upgrade.entity_type or lower_upg.group != upgrade.group or lower_upg.level >= upgrade.level:
            continue

        if not lower_upg.id in entity.upgrades:
            return False
    
    team = game.teams[entity.team]
    for [res, qty] in upgrade.cost.items():
        if team.resources[res] < qty:
            return False
    
    return True

def upgrade(game: gs.GameState, entity: en.Entity, upgrade: Upgrade):
    if not can_upgrade(game, entity, upgrade):
        return
    
    entity.upgrades.append(upgrade.id)
    team = game.teams[entity.team]
    for [res, qty] in upgrade.cost.items():
        team.resources[res] -= qty
    
    if upgrade.inc_attack != -1:
        entity.attack_speed = upgrade.inc_attack

    if upgrade.inc_hp != -1:
        ratio = upgrade.inc_hp/entity.max_hp
        entity.max_hp = upgrade.inc_hp
        entity.hp = round(ratio * entity.hp)
    
    if upgrade.inc_speed != -1:
        entity.speed = upgrade.inc_speed
