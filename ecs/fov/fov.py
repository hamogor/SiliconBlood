from constants import *
from ecs.fov.fov_component import FovComponent
from ecs.display.display import CameraComponent
from ecs.movement.movement_component import MovementComponent
import tcod
import pysnooper


class FovSystem:
    def __init__(self, game_map=None):
        self.game_map = game_map
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        for y in range(GRIDWIDTH):
            for x in range(GRIDHEIGHT):
                tcod.map_set_properties(self.fov_map, x, y,
                                        not game_map[x][y].block_path,
                                        not game_map[x][y].block_path)

    def update(self, entities):
        for e in entities:
            if e.get(FovComponent).fov_recalculate:
                tcod.map_compute_fov(
                    self.fov_map,
                    e.get(MovementComponent).x,
                    e.get(MovementComponent).y,
                    FOV_RADIUS,
                    FOV_LIGHT_WALLS,
                    0)
                e.get(FovComponent).fov_map = self.fov_map

