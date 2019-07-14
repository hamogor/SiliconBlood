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
        self.camera = Camera(GRIDWIDTH, GRIDHEIGHT)
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)

    def update(self, entities):
        for e in entities:
            if e.get(FovComponent).fov_recalculate:
                dc = e.get(DisplayComponent)
                if not dc.off_grid:
                    for x in range(0, GRIDWIDTH):
                        for y in range(0, GRIDHEIGHT):
                            visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                            self._root_display.blit(S_FOG, (x * TILESIZE, y * TILESIZE))
                            if visible:
                                if self.map.tiles[x][y].block_path:
                                    self._root_display.blit(S_WALL, (x * TILESIZE, y * TILESIZE))
                                else:
                                    self._root_display.blit(S_FLOOR, (x * TILESIZE, y * TILESIZE))
                                self.map.tiles[x][y].explored = True
                            elif self.map.tiles[x][y].explored:
                                if self.map.tiles[x][y].block_path:
                                    self._root_display.blit(S_DWALL, (x * TILESIZE, y * TILESIZE))
                                else:
                                    self._root_display.blit(S_DFLOOR, (x * TILESIZE, y * TILESIZE))
                    self._root_display.blit(S_PLAYER, (dc.x, dc.y))
                else:
                    self.map = GameMap()

        pygame.display.flip()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.move(self.camera.topleft)

    def update(self, entity):
        x = -entity.rect.x + int(WIDTH / 2)
        y = -entity.rect.y + int(HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)


