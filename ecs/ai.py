from ecs.actor import get_blocking_entities_at_location

import constants
import tcod
import math


class ComAi:
    def take_turn(self, target, game_map, game_objects):
        dx = tcod.random_get_int(0, -1, 1)
        dy = tcod.random_get_int(0, -1, 1)
        self.owner.move(dx, dy, game_map, game_objects)


def death_monster(monster):
    print(monster.creature.name_instance + " is dead!")
    monster.creature = None
    monster.ai = None
