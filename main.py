# 3rd party modules
import tcod as libtcod
import pygame

import constants


def game_main_loop():

    game_quit = False

    while not game_quit:

        # Get player input
        events_list = pygame.event.get()

        # Process input
        for event in events_list:
            if event.type is pygame.QUIT:
                game_quit = True

        # Draw the game
        draw_game()

    pygame.quit()
    exit()


def game_initialize():

    global SURFACE_MAIN

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))


def draw_game():
    global SURFACE_MAIN

    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    SURFACE_MAIN.blit(constants.S_PLAYER, (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2))

    pygame.display.flip()



if __name__ == '__main__':
    game_initialize()
    game_main_loop()
