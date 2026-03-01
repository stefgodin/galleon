import pygame
import scripts.game_state as gs
import scripts.assets as ast

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
    gold: int = 0
    rhum: int = 0
    wood: int = 0
    color: pygame.Color|int|str|tuple[int, int, int] = 'black'

def add_team(game: gs.GameState):
    idx = game.teams.__len__()
    team = Team()
    team.id = idx
    team.can_win = True
    team.gold = 0
    team.rhum = 0
    team.wood = 0
    team.color = TEAM_COLORS[idx % TEAM_COLORS.__len__()]

    game.teams.append(team)
    return idx

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
    pygame.draw.rect(render_target, 'grey', (modal_x, modal_y, w * 0.8, h * 0.8))
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
        team_text = info_font.render(team.id.__str__(), True, 'black')
        [tw, th] = team_text.get_size()
        team_square.blit(team_text, ((team_sqr_s - tw)/2, (team_sqr_s - th)/2, tw, th))
        line_renders.append(team_square)

        # Capture count
        team_capture_count = capture_by_team[team.id] if team.id in capture_by_team else 0
        capture_count_text = info_font.render(team_capture_count.__str__(), True, 'black')
        line_renders.append(capture_count_text)

        # Resources
        for res in (team.gold, team.rhum, team.wood):
            team_res_text = info_font.render(res.__str__(), True, 'black')
            line_renders.append(team_res_text)
        
        table_renders.append(line_renders)
    
    col_count = header_col.__len__()
    row_count = table_renders.__len__()
    columns_w = [0] * col_count
    row_h = 0
    for row in table_renders:
        i = 0
        for cell in row:
            [cell_w, cell_h] = cell.get_size()
            columns_w[i] = columns_w[i] if columns_w[i] >= cell_w else cell_w
            row_h = row_h if row_h >= cell_h else cell_h
            i += 1
    
    margin = 10
    padding = 10
    table = pygame.Surface((
        margin * 2 + padding * (col_count - 1) + sum(columns_w),
        margin * 2 + (padding + row_h) * row_count - padding,
    ))
    table.fill('white')
    cell_y = margin
    for i in range(0, row_count):
        cell_x = margin
        for j in range(0, col_count):
            col_w = columns_w[j]

            cell = table_renders[i][j]
            [cell_w, cell_h] = cell.get_size()
            table.blit(cell, (cell_x + (col_w - cell_w)/2, cell_y + (row_h - cell_h)/2))

            cell_x += (col_w + padding)

        cell_y += (row_h + padding)
    
    render_target.blit(table, (modal_x + padding, modal_y + padding))