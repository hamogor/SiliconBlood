from structs.level_gen import LevelGenerator


# TODO - Proper level storage and generate next level after first one has been loaded
class LevelSystem:
    def __init__(self, dungeon_level):
        self.map = LevelGenerator()
        self.tiles = self.map.level
        self.next_level = False
        self.dungeon_level = dungeon_level

    def generate_next_level(self):
        self.dungeon_level += 1
        self.__init__(dungeon_level=1)

    def update(self, entities):
        if self.next_level:
            self.generate_next_level()
