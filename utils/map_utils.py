from settings import GRIDWIDTH, GRIDHEIGHT


def check_for_wall(x, y, tiles):
    if (x < 0 or
            y < 0 or
            x >= GRIDWIDTH or
            y >= GRIDHEIGHT):
        return False

    else:
        return tiles[x][y].block_path
