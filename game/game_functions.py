# 3rd party modules
import pygame
# game files
import constants
from drawing.draw_functions import draw_game
from ecs.actor import ObjActor
from ecs.creature import ComCreature
from ecs.ai import ComAi
from map.game_map import GameMap
import pysnooper

#@pysnooper.snoop()
def game_main_loop():
    game_quit = False

    while True:
        action = game_handle_keys()
        if action:
            action[0](action[1])
        game_handle_keys()
        draw_game(SURFACE_MAIN, GAME_MAP, GAME_OBJECTS)


#@pysnooper.snoop()
def game_handle_keys():
    # get player input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return game_quit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return PLAYER.move, (0, -1)

            if event.key == pygame.K_DOWN:
                return PLAYER.move, (0, 1)

            if event.key == pygame.K_LEFT:
                return PLAYER.move, (-1, 0)

            if event.key == pygame.K_RIGHT:
                return PLAYER.move, (1, 0)


def game_quit():
    pygame.quit()
    exit()


def game_initialize():

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    GAME_MAP = GameMap(constants.MAP_HEIGHT, constants.MAP_WIDTH)

    creature_com1 = ComCreature("greg")
    PLAYER = ObjActor(0, 0, "python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = ComCreature("WigWig")
    ai_com = ComAi()
    ENEMY = ObjActor(15, 15, "WigWig", constants.S_WIGWIG, creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]