from ecs.fov.fov_component import FovComponent
from ecs.movement.movement_component import MovementComponent
from structs.game_map import GameMap
from constants import *
import pygame
import tcod
import pysnooper


class DisplaySystem:

    def __init__(self):
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = GameMap(generate=True)
        self.camera = Camera()

    def update(self, entities):
        for e in entities:
            self.camera.update(e)
            if e.get(FovComponent).fov_recalculate:
                for x in range(0, CAM_WIDTH):
                    for y in range(0, CAM_HEIGHT):
                        k, j = self.camera.apply(x, y)
                        wall = self.map.tiles[x][y].block_path
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        if visible:
                            if wall:
                                print("XY {} {}".format(x, y))
                                self._root_display.blit(S_WALL, (k * TILESIZE, j * TILESIZE))
                                print("KJ {} {}".format(k, j))
                            else:
                                self._root_display.blit(S_FLOOR, (k * TILESIZE, j * TILESIZE))
                            self.map.tiles[x][y].explored = True
                        elif self.map.tiles[k][j].explored:
                            if self.map.tiles[k][j].block_path:
                                self._root_display.blit(S_DWALL, (k * TILESIZE, j * TILESIZE))
                            else:
                                self._root_display.blit(S_DFLOOR, (k * TILESIZE, j * TILESIZE))

            self._root_display.blit(S_PLAYER, (15 * TILESIZE, 10 * TILESIZE))
        pygame.display.flip()


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = CAM_WIDTH
        self.height = CAM_HEIGHT
        self.map_width = GRIDWIDTH
        self.map_height = GRIDHEIGHT

    def apply(self, x, y):
        x = x + self.x
        y = y + self.y
        print("Apply: {} {}".format(x, y))
        return x, y

    def update(self, player):
        x = -player.get(MovementComponent).x + int(self.width / 2)
        y = -player.get(MovementComponent).y + int(self.height / 2)
        #print("Update: {} {}".format(x, y))
        self.x, self.y = x, y