import pygame
import scripts.game_state as gs

class EntityType:
    UNDEFINED = -1
    BOAT = 0
    CITY = 1

class Entity:
    type: int = EntityType.UNDEFINED

    # Render
    sprite_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    sprite_id: pygame.Surface|None = None

    # Movement
    can_move = False
    current_tile: int = -1
    current_tile_dist: int = -1
    destination_tile: int = -1
    destination_tile_dist: int = -1
    path: list[int] = []
    direction: pygame.Vector2 = pygame.Vector2(0, 0)
    speed: int = 0

    # Combat
    can_fight = False
    team: int = 0
    hp: int = 0
    max_hp: int = 0
    attack_speed: int = 0
    last_shot_t: int = 0