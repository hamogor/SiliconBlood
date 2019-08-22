from settings import GRIDWIDTH, GRIDHEIGHT
from ecs.display.display_component import DisplayComponent


def check_for_wall(x, y, tiles):
    if (x < 0 or
            y < 0 or
            x >= GRIDWIDTH or
            y >= GRIDHEIGHT):
        return False

    else:
        return tiles[x][y].block_path


def check_for_corner_movement(x, y, direction, tiles):
    if not tiles[x + direction[0]][y].block_path and not tiles[x][y + direction[1]].block_path:
        return True
    else:
        return False



