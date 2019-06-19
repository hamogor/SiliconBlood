import tcod as libtcod

from input_handlers import handle_keys


def main():
    # Screen size
    screen_width = 80
    screen_height = 50

    # Set player position to middle of screen
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'Escape The Deepwoods', False)

    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        libtcod.console_set_default_foreground(con, libtcod.white)  # Set '@' character to white
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)  # Put our player in middle of screen
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()  # Draw

        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
