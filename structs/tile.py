class Tile:
    def __init__(self, block_path, block_sight, sprite=None, name=None):
        self.block_path = block_path
        self.block_sight = block_sight
        self.sprite = sprite
        self.explored = False
        self.name = name
