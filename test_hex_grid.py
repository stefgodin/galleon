import pygame
import scripts.hex_grid as grid
import scripts.game_state as gs
import scripts.assets as ast
from scripts.game_runner import GameRunner

class HexGridTest(GameRunner):
    # Called once at the start of the game
    @staticmethod
    def init(game_state: gs.GameState):
        ast.load_assets(game_state)
        grid.generate_grid(game_state)

    # Called on every input event
    @staticmethod
    def input(game_state: gs.GameState, evt: pygame.event.Event):
        if evt.type == pygame.MOUSEBUTTONDOWN:
            grid.give_me_tile()

    # Called every fixed tick based on tick_rate (simulation speed), is not tied to framerate
    @staticmethod
    def tick(game_state: gs.GameState):
        pass

    # Called once per frame for real-time updates (or interpolation)
    @staticmethod
    def update(game_state: gs.GameState):
        pass

    # Called once per frame to redraw
    @staticmethod
    def render(game_state: gs.GameState, render_target: pygame.Surface):
        grid.draw_grid(game_state,render_target)
        # grid.highlight_current_tile(render_target)

HexGridTest().run()