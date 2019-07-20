from ecs.fov.fov_component import FovComponent
from ecs.movement.movement_component import MovementComponent
from ecs.camera.camera import Camera
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
                for cam_y in range(0, CAM_WIDTH):
                    for cam_x in range(0, CAM_HEIGHT):
                        x, y = self.camera.apply(cam_x, cam_y)
                        wall = self.map.tiles[x][y].block_path
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        if visible:
                            if wall:
                                self._root_display.blit(S_WALL, (cam_x * TILESIZE, cam_y * TILESIZE))
                            else:
                                self._root_display.blit(S_FLOOR, (cam_x * TILESIZE, cam_y * TILESIZE))

                            self.map.tiles[x][y].explored = True

                        elif self.map.tiles[x][y].explored:
                            if self.map.tiles[x][y].block_path:
                                self._root_display.blit(S_DWALL, (cam_x * TILESIZE, cam_y * TILESIZE))
                            else:
                                self._root_display.blit(S_DFLOOR, (cam_x * TILESIZE, cam_y * TILESIZE))
                        else:
                            self._root_display.blit(S_FOG, (cam_x * TILESIZE, cam_y * TILESIZE))
        self._root_display.blit(S_PLAYER, ((e.get(MovementComponent).cur_x - self.camera.x) * TILESIZE,
                                           (e.get(MovementComponent).cur_y - self.camera.y) * TILESIZE))
        pygame.display.flip()





