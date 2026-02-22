import pygame
import scripts.game_state as gs

class GameRunner:
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Galleon")
        clock = pygame.time.Clock()

        game_state = gs.GameState()
        
        self.init(game_state)

        while not game_state.should_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state.should_close = True
                else:
                    self.input(game_state, event)
            
            diff_t = game_state.game_t - game_state.tick_t
            while diff_t >= game_state.tick_rate:
                diff_t -= game_state.tick_rate
                game_state.tick_t = game_state.tick_rate
                self.tick(game_state)

            self.update(game_state)

            screen.fill("white")
            self.render(game_state, screen)

            pygame.display.flip()

            game_state.delta_t = clock.tick(120)
            game_state.game_t += game_state.delta_t
            pygame.display.set_caption("Galleon (" + str(int(clock.get_fps())) + " fps)")

        pygame.quit()
        
    # Called once at the start of the game
    @staticmethod
    def init(game_state: gs.GameState):
        pass

    # Called on every input event
    @staticmethod
    def input(game_state: gs.GameState, evt: pygame.event.Event):
        pass

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
        pass