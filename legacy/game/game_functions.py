# 3rd party modules
import pygame
# game files
import constants as const
from drawing.draw_functions import draw_game
from ecs.actor import ObjActor
from ecs.creature import ComCreature
from ecs.ai import ComAi
from map.game_map import GameMap
from ecs.ai import death_monster
from functools import partial
from input.input_handlers import game_handle_keys


def game_main_loop():

    while True:
        action = game_handle_keys(PLAYER)

        if action:
            action()
            game_take_turn()

        game_handle_keys(PLAYER)

        draw_game(SURFACE_MAIN, GAME_MAP, GAME_OBJECTS)


def game_take_turn():
    for obj in GAME_OBJECTS:
        if obj.ai:
            obj.ai.take_turn(PLAYER, GAME_MAP, GAME_OBJECTS)


def game_initialize():

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialize pygame
    pygame.init()
    pygame.display.set_caption("Silicon Blood")
    SURFACE_MAIN = pygame.display.set_mode((const.MAP_WIDTH * const.CELL_WIDTH,
                                            const.MAP_HEIGHT * const.CELL_HEIGHT))

    GAME_MAP = GameMap(const.MAP_HEIGHT, const.MAP_WIDTH)

    creature_com1 = ComCreature("Oref")
    PLAYER = ObjActor(5, 5, "Player", const.S_PLAYER, creature=creature_com1)

    creature_com2 = ComCreature("Enemy", death_function=death_monster)
    ai_com = ComAi()
    ENEMY = ObjActor(15, 15, "Enemy", const.S_ENEMY, creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [ENEMY, PLAYER]


def game_quit():
    pygame.quit()
    exit()
