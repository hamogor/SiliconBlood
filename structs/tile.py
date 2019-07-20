class StrucTile:
    def __init__(self, block_path, block_sight, sprite=None, dark_sprite=None):
        self.block_path = block_path
        self.block_sight = block_sight
        self.sprite = sprite
        self.dark_sprite = dark_sprite
        self.explored = False
