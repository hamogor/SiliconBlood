from structs.game_map import GameMap


class LevelSystem:
    __slots__ = ['level_map', 'items', 'dungeon_level']

    def __init__(self, dungeon_level):
        self.level_map = GameMap()
        self.items = None
        self.dungeon_level = dungeon_level

    def update(self, entities):
        pass
