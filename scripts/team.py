import pygame
import scripts.game_state as gs

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