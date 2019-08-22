from structs.level_gen import LevelGenerator


class LevelSystem:
    def __init__(self, dungeon_level):
        self.dungeon_level = dungeon_level
        self.map = LevelGenerator()
        self.level = self.map.level
        self.next_level = False

    def generate_next_level(self):
        self.dungeon_level += 1
        self.__init__(self.dungeon_level)

    def update(self, entities):
        if self.next_level:
            self.generate_next_level()
