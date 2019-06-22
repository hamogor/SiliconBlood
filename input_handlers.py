import tcod as libtcod
from enum import Enum


def handle_keys(key):
    # Movement keys
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    if key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    if key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    if key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == libtcod.KEY_CHAR:
        if key.c == ord('h'):
            return {'move': (-1, 0)}
    if key.vk == libtcod.KEY_CHAR:
        if key.c == ord('j'):
            return {'move': (0, 1)}
    if key.vk == libtcod.KEY_CHAR:
        if key.c == ord('k'):
            return {'move': (0, -1)}
    if key.vk == libtcod.KEY_CHAR:
        if key.c == ord('l'):
            return {'move': (1, 0)}
    if key.vk == left:
        return {'move': (0, -1)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle fullscreen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
