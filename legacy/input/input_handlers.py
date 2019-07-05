import constants as const
from functools import partial
import pygame

pygame.init()


def game_handle_keys(player):
    # get player input
    events_list = pygame.event.get()

    # process input3
    for event in events_list:
        if event.type == pygame.QUIT:
            return game_quit

        if event.type == pygame.KEYDOWN:

            if event.key in const.MOVE_N:
                return partial(player.move, 0,  -1, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_S:
                return partial(player.move, 0, 1, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_E:
                return partial(player.move, 1, 0, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_W:
                return partial(player.move, -1, 0, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_NW:
                return partial(player.move, -1, -1, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_NE:
                return partial(player.move, 1, -1, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_SW:
                return partial(player.move, -1, 1, GAME_MAP, GAME_OBJECTS)

            if event.key in const.MOVE_SE:
                return partial(player.move, 1, 1, GAME_MAP, GAME_OBJECTS)

            if event.key == pygame.K_ESCAPE:
                return partial(game_quit)


def game_quit():
    pygame.quit()
    exit()