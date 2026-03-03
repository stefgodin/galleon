import pygame
import scripts.game_state as gs
import scripts.assets as ast

class EntityType:
    BOAT = 0
    CITY = 1
    COVE = 2

class Entity:
    id: int = -1
    type: int = -1

    # Render
    sprite_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    sprite_id: str|None = None

    # Movement
    can_move: bool = False
    intangible: bool = False
    current_tile: int = -1
    prev_tile: int = -1
    next_tile: int = -1
    next_tile_dist: float = 0.0
    path: list[int] = []
    direction: pygame.Vector2 = pygame.Vector2(0, 0)
    speed: int = 0 # in ticks/tile

    # Combat
    can_attack: bool = False
    can_be_attacked: bool = False
    defeated: bool = False
    team: int = 0
    hp: int = 0
    max_hp: int = 0
    min_hp: int = 0
    attack_speed: int = 0 # in ticks/attack
    last_shot_t: int = 0
    can_capture: bool = False
    can_be_captured: bool = False
    capture_reset_stats: bool = False
    initial_max_hp: int = -1
    initial_attack_speed: int = -1
    capture_timer: int = 0
    max_capture_timer: int = 0
    capture_team: int = -1
    capture_contested: bool = False

    is_respawn_point: bool = False
    respawn_timer: int = 0
    max_respawn_timer: int = 0

    is_win_condition: bool = False

    # Resource
    can_yield_resources: bool = False
    resource_a: int = -1
    resource_b: int = -1
    gold_yield: int = 0
    rhum_yield: int = 0
    wood_yield: int = 0
    resource_yield_timer: int = 0
    max_resource_yield_timer: int = 0
    upgrades: list[int] = []
    show_upgrades: bool = False

def add_boat(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    boat_rect = pygame.Rect(0, 0, game.boat_base_size, game.boat_base_size)
    boat = Entity()
    boat.id = idx
    boat.type = EntityType.BOAT

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

    boat.can_attack = True
    boat.can_be_attacked = True
    boat.defeated = False
    boat.team =  0
    boat.hp =  10
    boat.max_hp =  10
    boat.attack_speed = 20
    boat.last_shot_t =  0
    boat.can_capture = True
    boat.respawn_timer = 0
    boat.max_respawn_timer = 160

    boat.upgrades = []

    game.entities.append(boat)
    return idx

def add_city(game: gs.GameState) -> int:
    idx = game.entities.__len__()
    city = Entity()
    city.id = idx
    city.type = EntityType.CITY
    city.current_tile = -1

    city.can_attack = True
    city.can_be_attacked = True
    city.defeated = False
    city.hp = 8
    city.max_hp = 8
    city.initial_max_hp = city.max_hp
    city.team = 0
    city.attack_speed = 20
    city.initial_attack_speed = city.attack_speed
    city.last_shot_t = 0
    city.can_be_captured = True
    city.capture_reset_stats = True
    city.can_capture = False
    city.capture_timer = 0
    city.max_capture_timer = 160
    city.capture_team = -1
    city.capture_contested = False

    city.is_win_condition = True

    city.can_yield_resources = True
    city.resource_yield_timer = 0
    city.max_resource_yield_timer = 800
    city.upgrades = []

    game.entities.append(city)
    return idx

def add_cove(game: gs.GameState):
    idx = game.entities.__len__()
    cove = Entity()
    cove.id = idx
    cove.type = EntityType.COVE
    cove.current_tile = -1

    cove.can_attack = True
    cove.can_be_attacked = False
    cove.defeated = False
    cove.hp = 1
    cove.max_hp = 1
    cove.min_hp = 1
    cove.team = 0
    cove.attack_speed = 10
    cove.last_shot_t = 0
    cove.is_respawn_point = True

    game.entities.append(cove)
    return idx