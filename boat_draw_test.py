import pygame
from scripts.boat import add_boat,load_boat_assets
from scripts.game_state import GameState

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    game = GameState()
    load_boat_assets(game)
    boat_1 = add_boat(game)

    while running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                game.mouse_pos.x = mouse_pos[0]
                game.mouse_pos.y = mouse_pos[1]
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = pygame.mouse.get_pressed()
                game.mouse_left = mouse_pressed[0]
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                game.key_1 = keys[pygame.K_1]
        
        # Update
        game.show_boxes = game.key_1

        if game.mouse_left:
            game.boat_going_to[boat_1] = game.mouse_pos.copy()

        for i, boat_going_to in enumerate(game.boat_going_to):
            if boat_going_to == None:
                continue

            movement = game.boat_speed_const * game.boat_speed[i] * game.dt

            x_done = False
            left_x = boat_going_to.x - game.boat_rect[i].x - (game.boat_rect[i].w/2)
            game.boat_direction[i].x = 1 if left_x >= 0 else -1
            mov_x = movement * game.boat_direction[i].x
            if abs(left_x) <= abs(mov_x):
                game.boat_rect[i].x = boat_going_to.x - (game.boat_rect[i].w / 2)
                x_done = True
            else:
                game.boat_rect[i].x += mov_x
                
            y_done = False
            left_y = boat_going_to.y - game.boat_rect[i].y - (game.boat_rect[i].h/2)
            game.boat_direction[i].y = 1 if left_y >= 0 else -1
            mov_y = movement * game.boat_direction[i].y
            if abs(left_y) <= abs(mov_y):
                game.boat_rect[i].y = boat_going_to.y - (game.boat_rect[i].h / 2)
                y_done = True
            else:
                game.boat_rect[i].y += mov_y
            
            if x_done and y_done:
                game.boat_going_to[i] = None
                

        # Render
        screen.fill("white")

        for i, boat_rect in enumerate(game.boat_rect):
            boat_img = game.boat_img[i]
            if game.boat_direction[i].x == 1:
                boat_img = pygame.transform.flip(boat_img, True, False)

            screen.blit(boat_img, boat_rect)

        if game.show_boxes:
            for boat_rect in game.boat_rect:
                pygame.draw.lines(screen, pygame.Color(255, 0, 0), True, [
                    (boat_rect.x, boat_rect.y),
                    (boat_rect.x + boat_rect.w, boat_rect.y),
                    (boat_rect.x + boat_rect.w, boat_rect.y + boat_rect.h),
                    (boat_rect.x, boat_rect.y + boat_rect.h),
                ])

        pygame.display.flip()

        game.dt = clock.tick(60)

    pygame.quit()

run()