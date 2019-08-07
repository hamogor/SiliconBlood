from structs.game_map import GameMap


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
