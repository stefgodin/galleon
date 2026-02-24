import pygame
import scripts.game_state as gs
import scripts.entity as en
import scripts.assets as ast

class EntityType:
    UNDEFINED = -1
    BOAT = 0
    CITY = 1

class Entity:
    type: int = EntityType.UNDEFINED

    # Render
    sprite_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    sprite_id: str|None = None

    # Movement
    can_move = False
    current_tile: int = -1
    prev_tile: int = -1
    next_tile: int = -1
    next_tile_dist: float = 0.0
    path: list[int] = []
    direction: pygame.Vector2 = pygame.Vector2(0, 0)
    speed: int = 0 # in ticks/tile

    # Combat
    can_fight = False
    defeated = False
    team: int = 0
    hp: int = 0
    max_hp: int = 0
    attack_speed: int = 0 # in ticks/attack
    last_shot_t: int = 0

def add_boat(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    boat_rect = pygame.Rect(0, 0, game.boat_base_size, game.boat_base_size)
    boat = en.Entity()
    boat.type = en.EntityType.BOAT

    boat.sprite_rect = boat_rect
    boat.sprite_id = ast.Assets.BOAT_BASE
    
    boat.can_move = True
    boat.current_tile = -1
    boat.prev_tile = -1
    boat.next_tile = -1
    boat.next_tile_dist = 0.0
    boat.path = []
    boat.direction = pygame.Vector2(0, 0)
    boat.speed = 20

    boat.can_fight = True
    boat.defeated = False
    boat.team =  0
    boat.hp =  10
    boat.max_hp =  10
    boat.attack_speed = 20
    boat.last_shot_t =  0

    game.entities.append(boat)
    return idx

def add_city(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    city = en.Entity()
    city.type = en.EntityType.CITY
    city.current_tile = -1

    city.can_fight = True
    city.defeated = False
    city.hp = 8
    city.max_hp = 8
    city.team = 0
    city.attack_speed = 20
    city.last_shot_t = 0

    game.entities.append(city)
    return idx