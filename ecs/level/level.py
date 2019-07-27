from structs.game_map import GameMap


class LevelSystem:
    __slots__ = ['level_map', 'items', 'dungeon_level', 'spawn_pos', 'level']

    def __init__(self, dungeon_level):
        self.level_map = GameMap()
        self.items = None
        self.dungeon_level = dungeon_level
        self.spawn_pos = ""
        self.set_spawn()
        self.level = ""

    def next_level(self):
        self.dungeon_level += 1
        self.__init__(dungeon_level=self.dungeon_level)

    def update(self, entities):
        pass

    def set_spawn(self):
        print(self.level_map.first_room)
        self.spawn_pos = self.level_map.first_room

