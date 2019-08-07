from structs.game_map import GameMap

# TODO - Proper level storage and generate next level after first one has been loaded
class LevelSystem:
    def __init__(self):
        self.level = GameMap().tiles
        self.next_level = False
        self.dungeon_level = 1

    def generate_next_level(self):
        pass

    def update(self, entities):
        if self.next_level:
            self.generate_next_level()
