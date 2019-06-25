import tcod as tcod
from entity import Entity
from input_handlers import handle_keys
from render_functions import clear_all, render_all

def main():
    screen_width = 80
    screen_height = 50

    # Middle of the screen
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    console = tcod.console_init_root(screen_width, screen_height, 'Escape The Deepwoods', False)

    player = Entity(player_x, player_y, '@', tcod.brass)
    npc = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.red)
    entities = [npc, player]

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        render_all(console, entities, screen_width, screen_height)

        tcod.console_flush()

        clear_all(console, entities)

        action = handle_keys(key)

        player.perform_action(action)

        if action.get('exit'):
            return True


if __name__ == '__main__':
    main()