import constants
from map.game_map import GameMap
import pysnooper



class ObjActor:
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x  # map address
        self.y = y  # map address
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self, surface_main):
        surface_main.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy, game_map, game_objects):
        tile_is_wall = game_map.tiles[self.x + dx][self.y + dy].block_path

        target = None

        for object in game_objects:
            if (object is not self and
                    object.x == self.x + dx and
                    object.y == self.y + dy and
                    object.creature):

                target = object
                break

        if target:
            print(self.creature.name_instance + " attacks " + target.creature.name_instance)
            target.creature.take_damage(5)

        if not tile_is_wall and target is None:
            self.x += dx
            self.y += dy
