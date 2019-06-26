import tcod as tcod


def render_all(console, entities, game_map, screen_width, screen_height):
    from pprint import pprint as pp
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                tcod.console_put_char_ex(console, x, y, '#', tcod.white, tcod.black)
            else:
                tcod.console_put_char_ex(console, x, y, '.', tcod.white, tcod.black)

    for entity in entities:
        draw_entity(console, entity)

    tcod.console_blit(console, 0, 0, screen_width, screen_height, console, 0, 0)


def clear_all(console, entities):
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console, entity):
    tcod.console_set_default_foreground(console, entity.fcolor)
    tcod.console_put_char_ex(console, entity.x, entity.y, entity.char, entity.fcolor, tcod.black)


def clear_entity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ', tcod.BKGND_NONE)
