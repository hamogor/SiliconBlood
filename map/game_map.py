from structs.tile import StrucTile
import constants
from random import randint
import pysnooper


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.generate_map()

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

        return False

    def initialize_tiles(self):
        tiles = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]

        for x in range(constants.MAP_WIDTH):
            tiles[x][0].block_path = True
            tiles[x][constants.MAP_HEIGHT-1].block_path = True

        for y in range(constants.MAP_HEIGHT):
            tiles[0][y].block_path = True
            tiles[constants.MAP_WIDTH - 1][y].block_path = True

        return tiles

    def cellular_automaton(self, tiles=None):
        chance_to_live = float(0.45)
        tiles = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]
        for x in range(constants.MAP_WIDTH):
            for y in range(constants.MAP_HEIGHT):
                if randint(0, 1) > chance_to_live:
                    tiles[x][y].block_path = True
        return tiles

    def count_alive_neighbours(self, tiles, x, y):
        count = 0
        i = -1
        j = -1
        for i in range(i, 2, 1):
            for j in range(j, 2, 1):
                neighbour_x = x+i
                neighbour_y = y+j
                if i == 0 and j == 0:
                    pass
                elif neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= len(tiles) or neighbour_y >= len(tiles[0]):
                    count += 1
                elif tiles[neighbour_x][neighbour_y].block_path:
                    count += 1

        return count

    def do_ca_step(self, old_map):
        new_map = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]
        for x in range(len(old_map)):
            for y in range(len(old_map[0])):
                nbs = self.count_alive_neighbours(old_map, x, y)
                if old_map[x][y].block_path:
                    if nbs < 2:
                        new_map[x][y].block_path = False
                    else:
                        new_map[x][y].block_path = True
                else:
                    if nbs == 3:
                        new_map[x][y].block_path = True
                    else:
                        new_map[x][y].block_path = False

        return new_map

    def generate_map(self):
        tiles = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]
        cell_map = self.cellular_automaton(tiles)
        for i in range(20):
            cell_map = self.do_ca_step(cell_map)

        return cell_map
