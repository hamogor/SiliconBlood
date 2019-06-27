from structs.tile import StrucTile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

        return False

    def initialize_tiles(self):
        tiles = [[StrucTile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[10][10].block_path = True
        tiles[10][15].block_path = True

        return tiles
