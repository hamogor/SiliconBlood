from ecs.fov.fov_component import FovComponent
from ecs.movement.movement_component import MovementComponent
from ecs.display.display_component import DisplayComponent
import pygame
import tcod
import sys

from settings import WIDTH, HEIGHT, CAM_WIDTH, CAM_HEIGHT, TILESIZE, S_FOG


class DisplaySystem:
    def __init__(self, level, camera):

        self.map = level.level_map
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.camera = camera

    def update(self, entities):
        for e in entities:
            self.camera.update(e)
            if e.get(FovComponent).fov_recalculate:
                for cam_y in range(0, CAM_WIDTH):
                    for cam_x in range(0, CAM_HEIGHT):
                        x, y = self.camera.apply(cam_x, cam_y)
                        block_path = self.map.tiles[x][y].block_path
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
                        sprite = self.map.tiles[x][y].sprite
                        if visible:
                            if block_path:
                                self._root_display.blit(sprite, (put_x, put_y))
                            else:
                                self._root_display.blit(sprite, (put_x, put_y))

                            self.map.tiles[x][y].explored = True

                        elif self.map.tiles[x][y].explored:
                            dark_sprite = self.map.tiles[x][y].dark_sprite
                            if block_path:
                                self._root_display.blit(dark_sprite, (put_x, put_y))
                            else:
                                self._root_display.blit(dark_sprite, (put_x, put_y))
                        else:
                            self._root_display.blit(S_FOG, (put_x, put_y))
            self._root_display.blit(e.get(DisplayComponent).sprite,
                                    ((e.get(MovementComponent).x - self.camera.x) * TILESIZE,
                                    (e.get(MovementComponent).y - self.camera.y) * TILESIZE))
            pygame.display.flip()
