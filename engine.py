import tcod as tcod
from entities.player import Player
from input_handlers import handle_keys

def main():
    screen_width = 80
    screen_height = 50

    # Middle of the screen
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    console = tcod.console_init_root(screen_width, screen_height, 'Escape The Deepwoods', False)

    player = Player('@', player_x, player_y)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        tcod.console_set_default_foreground(console, tcod.brass)

        tcod.console_put_char(console, player.x, player.y, '@', tcod.BKGND_NONE)

        tcod.console_blit(console, 0, 0, screen_width, screen_height, console, 0, 0)

        tcod.console_flush()

        tcod.console_put_char(console, player.x, player.y, ' ', tcod.BKGND_NONE)

        action = handle_keys(key)

        player.perform_action(action)

        if player.exit_signal:
            return True


if __name__ == '__main__':
    main()