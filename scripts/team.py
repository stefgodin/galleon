import pygame
import scripts.game_state as gs
import scripts.assets as ast
import scripts.entity_resource as en_res
import scripts.ui as ui

TEAM_COLORS = [
    "#607D8B",
    "#4CAF50",
    "#F44336",
    "#2196F3",
    "#FFEB3B",
    "#FF9800",
    "#00BCD4",
    "#673AB7",
]

class Team:
    id: int = -1
    can_win: bool = True
    resources: dict[int, int] = {}
    color: pygame.Color|int|str|tuple[int, int, int] = "black"

def add_team(game: gs.GameState):
    idx = game.teams.__len__()
    team = Team()
    team.id = idx
    team.can_win = True
    team.resources = {
        en_res.Resources.GOLD: 0,
        en_res.Resources.RHUM: 0,
        en_res.Resources.WOOD: 0,
    }
    team.color = TEAM_COLORS[idx % TEAM_COLORS.__len__()]

    game.teams.append(team)
    return idx

# Sets up the number of teams given + the default neutral team
def setup_teams(game: gs.GameState, count: int):
    t_id = add_team(game) # Neutral team (default)
    game.teams[t_id].can_win = False

    for _ in range(0, count):
        add_team(game)

def draw_team_info(game: gs.GameState, render_target: pygame.Surface):
    info_font = game.assets[ast.Assets.MAIN_FONT]
    [w, h] = render_target.get_size()
    modal_x = w * 0.1
    modal_y = h * 0.1
    pygame.draw.rect(render_target, "grey", (modal_x, modal_y, w * 0.8, h * 0.8))
    i = 0

    capture_by_team = {}
    for entity in game.entities:
        if entity.can_be_captured:
            capture_by_team[entity.team] = capture_by_team[entity.team] + 1 if entity.team in capture_by_team else 1

    table_renders: list[list[pygame.Surface]] = []
    header_col = [
        info_font.render("Team", True, "black"),
        info_font.render("Cities", True, "black"),
        info_font.render("Gold", True, "black"),
        info_font.render("Rhum", True, "black"),
        info_font.render("Wood", True, "black"),
    ]
    table_renders.append(header_col)
    
    for team in game.teams:
        if not team.can_win:
            continue

        line_renders = []

        # Color
        team_sqr_s = 40
        team_square = pygame.Surface((team_sqr_s, team_sqr_s))
        team_square.fill(team.color)
        team_text = info_font.render(team.id.__str__(), True, "black")
        [tw, th] = team_text.get_size()
        team_square.blit(team_text, ((team_sqr_s - tw)/2, (team_sqr_s - th)/2, tw, th))
        line_renders.append(team_square)

        # Capture count
        team_capture_count = capture_by_team[team.id] if team.id in capture_by_team else 0
        capture_count_text = info_font.render(team_capture_count.__str__(), True, "black")
        line_renders.append(capture_count_text)

        # Resources
        for res in (en_res.Resources.GOLD, en_res.Resources.RHUM, en_res.Resources.WOOD):
            team_res_text = info_font.render(team.resources[res].__str__(), True, "black")
            line_renders.append(team_res_text)
        
        table_renders.append(line_renders)
    
    grid = ui.align_in_grid(table_renders, row_padding=10, col_padding=10, margin=10)
    
    render_target.blit(grid, (modal_x + 10, modal_y + 10))