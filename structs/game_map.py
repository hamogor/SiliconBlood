from structs.tile import StrucTile
from settings import *
from random import uniform


class GameMap:
    def __init__(self):
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.tiles = self.generate_level()

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

        return False

    def cellular_gen(self, tiles):
        chance_to_live = float(0.72)
        for x in range(self.width):
            for y in range(self.height):
                if uniform(0, 1) > chance_to_live:
                    tiles[x][y].block_path, tiles[x][y].block_sight = True, True
                    tiles[x][y].sprite = S_WALL
                    tiles[x][y].dark_sprite = S_DWALL
                else:
                    tiles[x][y].sprite = S_FLOOR
                    tiles[x][y].dark_sprite = S_DFLOOR
        return tiles

    def count_alive_neighbours(self, tiles, x, y):
        count = 0
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                neighbour_x = x + i
                neighbour_y = y + j
                if i == 0 and j == 0:
                    pass
                elif neighbour_x < 0 or neighbour_y < 0 \
                        or neighbour_x >= self.width or neighbour_y >= self.height:
                    count += 1
                elif tiles[neighbour_x][neighbour_y].block_path:
                    count += 1
        return count

    def do_gen_step(self, old_map):
        new_map = [[StrucTile(False, False) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                neighbours = self.count_alive_neighbours(old_map, x, y)
                if old_map[x][y].block_path:
                    new_map[x][y].block_path = neighbours >= 3
                else:
                    new_map[x][y].block_path = neighbours > 4

        return new_map

    def generate_level(self):
        tiles = [[StrucTile(False, False) for y in range(self.height)] for x in range(self.width)]
        cell_map = self.cellular_gen(tiles)
        for i in range(4):
            cell_map = self.do_gen_step(cell_map)
        return cell_map