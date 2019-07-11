from constants import *
from ecs.fov.fov_component import FovComponent
from ecs.display.display_component import DisplayComponent
import tcod
import pysnooper


class FovSystem:
    def __init__(self, game_map=None):
        self.game_map = game_map
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        for y in range(GRIDHEIGHT):
            for x in range(GRIDWIDTH):
                tcod.map_set_properties(self.fov_map, x, y,
                                        not game_map[x][y].block_sight,
                                        not game_map[x][y].block_path)

    # TODO - Fix fov being initialised via DisplayComponent resolution
    def update(self, entities):
        for e in entities:
            if e.get(FovComponent).fov_recalculate:
                e.get(FovComponent).fov_recalculate = False
                tcod.map_compute_fov(
                    self.fov_map,
                    int(e.get(DisplayComponent).x / TILESIZE),
                    int(e.get(DisplayComponent).y / TILESIZE),
                    FOV_RADIUS,
                    FOV_LIGHT_WALLS,
                    FOV_ALGORITHM)
                e.get(FovComponent).fov_map = self.fov_map

