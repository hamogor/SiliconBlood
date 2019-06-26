# 3rd party modules
import tcod as libtcod
import pygame

import constants


class StrucTile:
    def __init__(self, block_path):
        self.block_path = block_path


def map_create():
    new_map = [[StrucTile(False) for y in range(0, constants.MAP_WIDTH)] for x in range(0, constants.MAP_HEIGHT)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map


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

    global SURFACE_MAIN, GAME_MAP

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    GAME_MAP = map_create()


def draw_game():
    global SURFACE_MAIN

    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    draw_map(GAME_MAP)

    SURFACE_MAIN.blit(constants.S_PLAYER, (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2))

    pygame.display.flip()


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path:
                SURFACE_MAIN.blit(constants.S_WALL, (x*constants.CELL_WIDTH, y*constants.CELL_WIDTH))
            else:
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_WIDTH))


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
