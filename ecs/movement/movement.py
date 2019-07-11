from ecs.movement.movement_component import MovementComponent
from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent
from constants import *
import pysnooper


class MovementSystem:
    def __init__(self, game_map):
        self.game_map = game_map

    # TODO - Stop moving diagonally if tile above and to the right is block_path
    def update(self, entities):
        for e in entities:
            cur_x = e.get(DisplayComponent).x
            cur_y = e.get(DisplayComponent).y

            d_x = e.get(MovementComponent).x
            d_y = e.get(MovementComponent).y

            if not self.game_map[d_x][d_y].block_path:
                e.get(FovComponent).fov_recalculate = True
                e.get(DisplayComponent).x = d_x * TILESIZE
                e.get(DisplayComponent).y = d_y * TILESIZE
            else:
                e.get(DisplayComponent).x = cur_x
                e.get(DisplayComponent).y = cur_y
                e.get(MovementComponent).x = int(cur_x / TILESIZE)
                e.get(MovementComponent).y = int(cur_y / TILESIZE)