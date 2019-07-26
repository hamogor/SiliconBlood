from structs.game_map import GameMap


class LevelSystem:
    __slots__ = ['level_map', 'items', 'dungeon_level', 'spawn_pos']

    def __init__(self, dungeon_level):
        self.level_map = GameMap()
        self.items = None
        self.dungeon_level = dungeon_level
        self.spawn_pos = []
        self.set_spawn()

    def update(self, entities):
        pass

    def set_spawn(self):
        self.spawn_pos.append(self.level_map.first_room)
