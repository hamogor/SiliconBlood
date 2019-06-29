# 3rd party modules
import pygame
# game files
import constants
from drawing.draw_functions import draw_game
from ecs.actor import ObjActor
from ecs.creature import ComCreature
from ecs.ai import ComAi
from map.game_map import GameMap
from ecs.ai import death_monster
from functools import partial


def game_main_loop():

    while True:
        action = game_handle_keys()

        if action:
            action()
            game_take_turn()

        game_handle_keys()

        draw_game(SURFACE_MAIN, GAME_MAP, GAME_OBJECTS)


def game_handle_keys():
    # get player input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return game_quit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return partial(PLAYER.move, 0, -1, GAME_MAP, GAME_OBJECTS)

            if event.key == pygame.K_DOWN:
                return partial(PLAYER.move, 0, 1, GAME_MAP, GAME_OBJECTS)

            if event.key == pygame.K_LEFT:
                return partial(PLAYER.move, -1, 0, GAME_MAP, GAME_OBJECTS)

            if event.key == pygame.K_RIGHT:
                return partial(PLAYER.move, 1, 0, GAME_MAP, GAME_OBJECTS)

            if event.key == pygame.K_ESCAPE:
                return partial(game_quit)


def game_take_turn():
    for obj in GAME_OBJECTS:
        if obj.ai:
            obj.ai.take_turn(GAME_MAP, GAME_OBJECTS)


def game_initialize():

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    GAME_MAP = GameMap(constants.MAP_HEIGHT, constants.MAP_WIDTH)

    creature_com1 = ComCreature("Oref")
    PLAYER = ObjActor(1, 1, "Player", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = ComCreature("WigWig", death_function=death_monster)
    ai_com = ComAi()
    ENEMY = ObjActor(15, 15, "WigWig", constants.S_WIGWIG, creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [ENEMY, PLAYER]


def game_quit():
    pygame.quit()
    exit()