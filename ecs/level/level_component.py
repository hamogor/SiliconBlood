class LevelComponent:
    def __init__(self, level_map, items, next_level=False):
        self.level_map = level_map
        self.items = items
        self.next_level = next_level
