import tcod


class ComAi:
    def take_turn(self, game_map, game_objects):
        dx = tcod.random_get_int(0, -1, 1)
        dy = tcod.random_get_int(0, -1, 1)
        self.owner.move(dx, dy, game_map, game_objects)
