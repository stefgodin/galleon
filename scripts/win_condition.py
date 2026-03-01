import pygame
import scripts.game_state as gs
import scripts.assets as ast

def setup_win_condition(game_state: gs.GameState):
    game_state.max_game_timer = 12000
    game_state.real_time_max_game_timer = 300

def tick_win_condition(game_state: gs.GameState):
    game_state.game_timer = min(game_state.game_timer + 1, game_state.max_game_timer)

    if game_state.game_timer != game_state.max_game_timer:
        return

    game_state.game_over = True

    team_capture_count_map = {}
    for entity in game_state.entities:
        if entity.team not in team_capture_count_map:
            team_capture_count_map[entity.team] = 0 
            
        if entity.is_win_condition:
            team_capture_count_map[entity.team] = team_capture_count_map[entity.team] + 1
    
    team_capture_count_map[0] = 0 # Neutral team shouldn't win unless no team have captured anything (then it's a draw)
    
    team_capture_count = sorted(team_capture_count_map.items(), key=lambda tc: tc[1])
    team_capture_count.reverse()
    if not team_capture_count.__len__():
        game_state.winner_team = -1
    else:
        if team_capture_count.__len__() > 1 and team_capture_count[0][1] == team_capture_count[1][1]:
            game_state.winner_team = -1
        else:
            game_state.winner_team = team_capture_count[0][0]

def draw_game_timer(game: gs.GameState, render_target: pygame.Surface):
    w = render_target.get_width()
    time_left = round((1 - game.game_timer/game.max_game_timer) * game.real_time_max_game_timer)
    secs = (time_left % 60).__str__().zfill(2)
    mins = int(time_left / 60).__str__()
    time = mins+":"+secs

    timer_font = game.assets[ast.Assets.MAIN_FONT]
    timer_text = timer_font.render(time, True, 'black')
    [tw, th] = timer_text.get_size()
    render_target.blit(timer_text, ((w - tw)/2, 24, tw, th))

def draw_game_over(game: gs.GameState, render_target: pygame.Surface):
    [w, h] = render_target.get_size()

    pygame.draw.rect(render_target, 'black', (0.08 * w, 0.08 * h, 0.84 * w, 0.84 * h))
    winner_color = game.teams[game.winner_team].color if game.winner_team != -1 else 'white'
    pygame.draw.rect(render_target, winner_color, (0.1 * w, 0.1 * h, 0.8 * w, 0.8 * h))

    text_font = game.assets[ast.Assets.MAIN_FONT]
    text = "Team "+ game.winner_team.__str__() + " won!" if game.winner_team != -1 else "Draw!"
    win_text = text_font.render(text, True, 'black')
    [tw, th] = win_text.get_size()
    render_target.blit(win_text, ((w - tw)/2, (h - th)/2, tw, th))