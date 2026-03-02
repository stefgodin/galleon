import pygame
import scripts.fake_grid as grid
import scripts.game_state as gs
import scripts.entity as en
import scripts.entity_resource as en_res
import scripts.entity_upgrade as en_upg
import scripts.assets as ast
import scripts.ui as ui

class DRAW_LAYERS:
    ENTITY = 0
    ENTITY_UI = 1

def draw_entities(game: gs.GameState, render_target: pygame.Surface):
    for layer in range(DRAW_LAYERS.ENTITY, DRAW_LAYERS.ENTITY_UI + 1):
        for entity in game.entities:
            match entity.type:
                case en.EntityType.BOAT:
                    draw_boat(game, render_target, entity, layer)
                case en.EntityType.CITY:
                    draw_city(game, render_target, entity, layer)
                case en.EntityType.COVE:
                    draw_cove(game, render_target, entity, layer)


def draw_boat(game: gs.GameState, render_target: pygame.Surface, boat: en.Entity, layer: int):
    team_color = game.teams[boat.team].color
    if layer == DRAW_LAYERS.ENTITY:
        boat_img = game.assets[boat.sprite_id]
        boat_img = pygame.transform.scale(boat_img, (game.boat_base_size, game.boat_base_size))
        if boat.direction.x == 1:
            boat_img = pygame.transform.flip(boat_img, True, False)

        render_target.blit(boat_img, boat.sprite_rect)
    elif layer == DRAW_LAYERS.ENTITY_UI:
        # Health bar
        [x, y] = boat.sprite_rect.midtop
        health_bar_width = 10 * boat.max_hp
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (health_bar_width/2) - 2, y - 12, health_bar_width + 4, 14])
        pygame.draw.rect(surface= render_target, color= "black", rect= [x - (health_bar_width/2), y - 10, health_bar_width, 10])
        pygame.draw.rect(surface= render_target, color= "red", rect= [x - (health_bar_width/2), y - 10, 10 * boat.hp, 10])

        draw_hit_boxes(game, render_target, boat)
        draw_upgrades_panel(game, render_target, boat)


def draw_city(game: gs.GameState, render_target: pygame.Surface, city: en.Entity, layer: int):
    team_color = game.teams[city.team].color
    [x, y] = grid.index_to_global_coord(game, city.current_tile)
    if layer == DRAW_LAYERS.ENTITY:
        pygame.draw.rect(surface= render_target, color= team_color, rect= [x - game.fake_grid_tile_size/2, y - game.fake_grid_tile_size/2, game.fake_grid_tile_size, game.fake_grid_tile_size])
    elif layer == DRAW_LAYERS.ENTITY_UI:
        if not city.defeated:
            # Health bar
            hp_bar_y = y - game.fake_grid_tile_size/2
            health_bar_w = 10 * city.max_hp
            pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (health_bar_w/2) - 2, hp_bar_y - 16, health_bar_w + 4, 14])
            pygame.draw.rect(surface= render_target, color= "black", rect= [x - (health_bar_w/2), hp_bar_y - 14, health_bar_w, 10])
            pygame.draw.rect(surface= render_target, color= "red", rect= [x - (health_bar_w/2), hp_bar_y - 14, city.hp/city.max_hp * health_bar_w, 10])
        else:
            # Capture progress
            capture_team_color = game.teams[city.capture_team].color if city.capture_team != -1 and not city.capture_contested else game.teams[0].color
            capture_bar_y = y - game.fake_grid_tile_size/2
            capture_timer_w = 10 * city.max_hp 
            pygame.draw.rect(surface= render_target, color= team_color, rect= [x - (capture_timer_w/2) - 2, capture_bar_y - 16, capture_timer_w + 4, 14])
            pygame.draw.rect(surface= render_target, color= "black", rect= [x - (capture_timer_w/2), capture_bar_y - 14, capture_timer_w, 10])
            pygame.draw.rect(surface= render_target, color= capture_team_color, rect= [x - (capture_timer_w/2), capture_bar_y - 14, city.capture_timer/city.max_capture_timer*capture_timer_w, 10])
        
        # Resource yield
        resource_timer_w = 10 * city.max_hp
        resource_timer_y = y - game.fake_grid_tile_size/2

        if city.resource_a != -1:
            pygame.draw.rect(surface= render_target, color= en_res.RESOURCE_COLORS[city.resource_a], rect= [x - (resource_timer_w/2), resource_timer_y, city.resource_yield_timer/city.max_resource_yield_timer * resource_timer_w, 4])

        if city.resource_b != -1:
            pygame.draw.rect(surface= render_target, color= en_res.RESOURCE_COLORS[city.resource_b], rect= [x - (resource_timer_w/2), resource_timer_y + 4, city.resource_yield_timer/city.max_resource_yield_timer * resource_timer_w, 4])

        draw_hit_boxes(game, render_target, city)
        draw_upgrades_panel(game, render_target, city)


def draw_cove(game: gs.GameState, render_target: pygame.Surface, cove: en.Entity, layer: int):
    if layer == DRAW_LAYERS.ENTITY:
        team_color = game.teams[cove.team].color
        [x, y] = grid.index_to_global_coord(game, cove.current_tile)
        if layer == DRAW_LAYERS.ENTITY:
            pygame.draw.rect(surface= render_target, color= "black", rect= [x - game.fake_grid_tile_size/2, y - game.fake_grid_tile_size/2, game.fake_grid_tile_size, game.fake_grid_tile_size])
            pygame.draw.rect(surface= render_target, color= team_color, rect= [x - game.fake_grid_tile_size/2 + 3, y - game.fake_grid_tile_size/2 + 3, game.fake_grid_tile_size - 6, game.fake_grid_tile_size - 6])

    elif layer == DRAW_LAYERS.ENTITY_UI:
        draw_hit_boxes(game, render_target, cove)


def draw_hit_boxes(game: gs.GameState, render_target: pygame.Surface, entity: en.Entity):
    # Boxes
    if not game.show_boxes:
        return 

    neihbors = grid.neighbor_tiles(game, entity.current_tile)
    for tile in neihbors:
        [x, y] = grid.index_to_global_coord(game, tile)
        s = game.fake_grid_tile_size
        pygame.draw.lines(render_target, game.teams[entity.team].color, True, [
            (x - s/2, y - s/2),
            (x + s/2, y - s/2),
            (x + s/2, y + s/2),
            (x - s/2, y + s/2),
        ])


def draw_upgrades_panel(game: gs.GameState, render_target: pygame.Surface, entity: en.Entity):
    if not entity.show_upgrades or entity.current_tile == -1 and not entity.defeated:
        return
    
    upgrade_groups: dict[str, list[en_upg.Upgrade]] = {}
    max_upgrade_group = 0
    for upgrade in game.upgrades:
        if upgrade.entity_type != entity.type:
            continue
        
        if upgrade.group not in upgrade_groups:
            upgrade_groups[upgrade.group] = []

        upgrade_groups[upgrade.group].append(upgrade)
        
        max_upgrade_group = max(upgrade_groups[upgrade.group].__len__(), max_upgrade_group)

    if max_upgrade_group == 0:
        return
    
    font = game.assets[ast.Assets.MAIN_FONT]

    upgrade_grid_content = []
    for group_upgrades in upgrade_groups.values():
        upgrade_group_line = []

        if entity.team == game.player_team:
            can_upgrade = False
            for upg in group_upgrades:
                if en_upg.can_upgrade(game, entity, upg):
                    can_upgrade = True
                    break

            upgrade_btn = pygame.Surface((40, 40))
            upgrade_btn.fill(("white" if can_upgrade else "#AEAEAE"))
            plus: pygame.Surface = font.render("+", True, "black")
            [plus_w, plus_h] = plus.get_size()
            upgrade_btn.blit(plus, ((40 - plus_w)/2, (40 - plus_h)/2))
            upgrade_group_line.append(upgrade_btn)

        for i in range(0, max_upgrade_group):
            upgrade = group_upgrades[i] if group_upgrades.__len__() > i else None
            upgrade_cell = None
            if upgrade != None:
                is_active = upgrade.id in entity.upgrades
                upgrade_cell = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
                upgrade_cell = upgrade_cell.convert_alpha()
                pygame.draw.circle(upgrade_cell, ("red" if is_active else "black"), (5, 5), 4)

            upgrade_group_line.append(upgrade_cell)
        
        upgrade_grid_content.append(upgrade_group_line)

    upgrade_grid = ui.align_in_grid(upgrade_grid_content, row_padding=5, col_padding=5, margin=10)

    upgrade_panel = pygame.Surface(upgrade_grid.get_size())
    upgrade_panel.fill("grey")
    [panel_w, panel_h] = upgrade_panel.get_size()

    upgrade_panel.blit(upgrade_grid, (0, 0))

    [entity_tile_x, entity_tile_y] = grid.index_to_global_coord(game, entity.current_tile)
    if entity.sprite_rect:
        entity_tile_x = entity.sprite_rect.centerx
        entity_tile_y = entity.sprite_rect.centery
    render_target.blit(upgrade_panel, (entity_tile_x - panel_w/2, entity_tile_y - game.fake_grid_tile_size/2 - 10 - panel_h))