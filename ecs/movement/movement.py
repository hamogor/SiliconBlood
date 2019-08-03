from ecs.movement.movement_component import MovementComponent
from structs.assets import Assets
from ecs.fov.fov_component import FovComponent


class MovementSystem:
    def __init__(self, level):
        self.assets = Assets()
        self.game_map = level.level_map

    def reset(self, level):
        self.__init__(level)

    def update(self, entities):
        for e in entities:
            self.move(e)

    def move(self, entity):
        current_x, current_y = entity.get(MovementComponent).x, entity.get(MovementComponent).y
        direction_x, direction_y = entity.get(MovementComponent).d_x, entity.get(MovementComponent).d_y
        wall = self.game_map.tiles[direction_x][direction_y].block_path

        if not wall:
            entity.get(FovComponent).fov_recalculate = True
            entity.get(MovementComponent).x = direction_x
            entity.get(MovementComponent).y = direction_y
        else:
            entity.get(MovementComponent).x = current_x
            entity.get(MovementComponent).y = current_y
            entity.get(MovementComponent).d_x = current_x
            entity.get(MovementComponent).d_y = current_y
            print("north: {}".format(self.game_map.tiles[entity.get(MovementComponent).x][entity.get(MovementComponent).y - 1].assignment))
            print("south: {}".format(self.game_map.tiles[entity.get(MovementComponent).x][entity.get(MovementComponent).y + 1].assignment))
            print("west: {}".format(self.game_map.tiles[entity.get(MovementComponent).x - 1][entity.get(MovementComponent).y].assignment))
            print("east: {}".format(self.game_map.tiles[entity.get(MovementComponent).x + 1][entity.get(MovementComponent).y].assignment))
            print("NE: {}".format(self.game_map.tiles[entity.get(MovementComponent).x + 1][entity.get(MovementComponent).y - 1].assignment))
            print("NW: {}".format(self.game_map.tiles[entity.get(MovementComponent).x - 1][entity.get(MovementComponent).y - 1].assignment))
            print("SE: {}".format(self.game_map.tiles[entity.get(MovementComponent).x + 1][entity.get(MovementComponent).y + 1].assignment))
            print("SW: {}".format(self.game_map.tiles[entity.get(MovementComponent).x - 1][entity.get(MovementComponent).y + 1].assignment))


