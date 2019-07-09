from constants import *
import tcod


class FovComponent:
    def __init__(self, fov_map=None):
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        self.fov_recalculate = True
