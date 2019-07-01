import tcod
import math


class ComAi:
    def take_turn(self, game_map, game_objects):
        dx = tcod.random_get_int(0, -1, 1)
        dy = tcod.random_get_int(0, -1, 1)
        self.move_towards(dx, dy)
        self.owner.move(dx, dy, game_map, game_objects)

    def move_towards(self, target_x, target_y, game_map, game_objects):
        dx = self.owner.x
        dy = self.owner.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        try:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))
        except ZeroDivisionError:
            print("Zero division error")
            print(dx)
            print(dy)
            print(distance)
        if not :
            self.owner.move(dx, dy, game_map, game_objects)


def death_monster(monster):
    print(monster.creature.name_instance + " is dead!")
    monster.creature = None
    monster.ai = None
