import tcod as libtcod
from enum import Enum


def handle_keys(key):
    key_char = chr(key.c)
    # Movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    if key.vk == libtcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    if key.vk == libtcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    if key.vk == libtcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    if key_char == 'q':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'z':
        return {'move': (-1, 1)}
    elif key_char == 'c':
        return {'move': (1, 1)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle fullscreen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
