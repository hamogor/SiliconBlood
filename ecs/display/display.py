from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent
from constants import *
from structs.game_map import GameMap
import pygame
import tcod
import pysnooper


class DisplaySystem:

    def __init__(self):
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = GameMap()

    def update(self, entities):
        for e in entities:
            dc = e.get(DisplayComponent)
            if e.get(FovComponent).fov_recalculate:
                for x in range(0, GRIDWIDTH):
                    for y in range(0, GRIDHEIGHT):
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map,
                                                     int(e.get(DisplayComponent).x / TILESIZE),
                                                     int(e.get(DisplayComponent).y / TILESIZE))
                        if not visible:
                            if self.map.tiles[x][y].block_path:
                                self._root_display.blit(S_WALL, (x * TILESIZE, y * TILESIZE))
                            else:
                                self._root_display.blit(S_FLOOR, (x * TILESIZE, y * TILESIZE))
                        else:
                            self._root_display.blit(S_FOG, (x * TILESIZE, y * TILESIZE))
            self._root_display.blit(S_PLAYER, (dc.x, dc.y))
        pygame.display.flip()
