from settings import FOV_LIGHT_WALLS, FOV_RADIUS, FOV_ALGORITHM, GRIDWIDTH, GRIDHEIGHT
from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent
import tcod

# TODO - Play with some fov algorithms
class FovSystem:
    def __init__(self, level):
        self.game_map = level
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        for y in range(GRIDWIDTH):
            for x in range(GRIDHEIGHT):
                tcod.map_set_properties(self.fov_map, x, y,
                                        not self.game_map[x][y].block_sight,
                                        not self.game_map[x][y].block_path)

    def update(self, entities):
        for e in entities:
            if e.has(FovComponent) and e.get(FovComponent).fov_recalculate:
                tcod.map_compute_fov(
                    self.fov_map,
                    e.get(DisplayComponent).x,
                    e.get(DisplayComponent).y,
                    FOV_RADIUS,
                    FOV_LIGHT_WALLS,
                    FOV_ALGORITHM)
                e.get(FovComponent).fov_map = self.fov_map
