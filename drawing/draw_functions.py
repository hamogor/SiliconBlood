import constants
import pygame


def draw_game(surface_main, map, objects):

    surface_main.fill(constants.COLOR_DEFAULT_BG)

    draw_map(surface_main, map)

    for obj in objects:
        obj.draw(surface_main)

    pygame.display.flip()


def draw_map(surface_main, map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw.tiles[x][y].block_path:
                # draw wall
                surface_main.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                surface_main.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))