import tcod as tcod
from entity import Entity
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
import constants as cons


def main():
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    console = tcod.console_init_root(cons.screen_width, cons.screen_height, 'Escape The Deepwoods', False)
    game_map = GameMap(cons.map_width, cons.map_height)
    player = Entity(cons.player_x, cons.player_y, '@', tcod.brass)
    npc = Entity(int(cons.screen_width / 2), int(cons.screen_height / 2), '@', tcod.red)
    entities = [npc, player]
    key = tcod.Key()
    mouse = tcod.Mouse()
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        render_all(console, entities, game_map, cons.screen_width, cons.screen_height)
        tcod.console_flush()
        clear_all(console, entities)
        action = handle_keys(key)
        player.perform_action(action, game_map)
        if action.get('exit'):
            return True


if __name__ == '__main__':
    main()