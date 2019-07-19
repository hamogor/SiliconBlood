from ecs.movement.movement_component import MovementComponent
from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent
from constants import *
import pysnooper


class MovementSystem:
    def __init__(self, game_map):
        self.game_map = game_map

    def update(self, entities):
        for e in entities:
            cur_x = int(e.get(MovementComponent).cur_x)
            cur_y = int(e.get(MovementComponent).cur_y)

            d_x = e.get(MovementComponent).x
            d_y = e.get(MovementComponent).y
            if not self.game_map[d_x][d_y].block_path:
                e.get(FovComponent).fov_recalculate = True
                e.get(MovementComponent).x = d_x
                e.get(MovementComponent).y = d_y
                e.get(MovementComponent).cur_x = e.get(MovementComponent).x
                e.get(MovementComponent).cur_y = e.get(MovementComponent).y


            else:
                e.get(MovementComponent).x = cur_x
                e.get(MovementComponent).y = cur_y
