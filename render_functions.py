import tcod as tcod


def render_all(console, entities, screen_width, screen_height):
    for entity in entities:
        draw_entity(console, entity)


    tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console, entities):
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console, entity):
    tcod.console_set_default_foreground(console, entity.color)
    tcod.console_put_char(console, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def clear_entity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ', tcod.BKGND_NONE)