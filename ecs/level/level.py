from structs.game_map import GameMap


class LevelSystem:
    def __init__(self):
        self.level_map = GameMap()
        self.items = None
        self.next_level = False

    def update(self, entities):
        pass
