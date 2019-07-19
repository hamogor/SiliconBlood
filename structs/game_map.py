from structs.tile import StrucTile
from constants import *
from random import uniform
import pysnooper


class GameMap:
    def __init__(self, generate=True):
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        if generate:
            self.tiles = self.generate_map()
        else:
            self.tiles = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

        return False

    @staticmethod
    def cellular_automaton(tiles):
        chance_to_live = float(0.72)
        for x in range(GRIDHEIGHT):
            for y in range(GRIDWIDTH):
                if uniform(0, 1) > chance_to_live:
                    tiles[x][y].block_path = True
                    tiles[x][y].block_sight = True
        return tiles

    def count_alive_neighbours(self, tiles, x, y):
        count = 0
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                neighbour_x = x+i
                neighbour_y = y+j
                if i == 0 and j == 0:
                    pass
                elif neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= self.width or neighbour_y >= self.height:
                    count += 1
                elif tiles[neighbour_x][neighbour_y].block_path:
                    count += 1
        return count

    def do_ca_step(self, old_map):
        new_map = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                nbs = self.count_alive_neighbours(old_map, x, y)
                # Living cells
                if old_map[x][y].block_path:
                    new_map[x][y].block_path = nbs >= 3
                else:
                    new_map[x][y].block_path = nbs > 4

        return new_map

    def generate_map(self):
        tiles = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]
        cell_map = self.cellular_automaton(tiles)
        for i in range(4):
            cell_map = self.do_ca_step(cell_map)
        return cell_map
