from ecs.fov.fov_component import FovComponent
from ecs.camera.camera_component import CameraComponent
from ecs.movement.movement_component import MovementComponent
from ecs.display.display_component import DisplayComponent
from settings import WIDTH, HEIGHT, CAM_WIDTH, CAM_HEIGHT, TILESIZE, S_FOG
import pygame
import tcod


class DisplaySystem:
    def __init__(self, level):

        self.map = level.level_map.tiles
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))

    def update(self, entities):
        for e in entities:
            if e.get(FovComponent).fov_recalculate:
                for cam_y in range(0, CAM_WIDTH):
                    for cam_x in range(0, CAM_HEIGHT):

                        x, y = e.get(CameraComponent).cam_x, e.get(CameraComponent).cam_y
                        block_path = self.map[x][y].block_path
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        put_x, put_y = x * TILESIZE, y * TILESIZE
                        sprite = self.map[cam_x][cam_y].sprite

                        if visible:
                            if block_path:
                                self._root_display.blit(sprite, (put_x, put_y))
                            else:
                                self._root_display.blit(sprite, (put_x, put_y))

                            self.map.explored = True

                        elif self.map[x][y].explored:
                            dark_sprite = self.map[cam_x][cam_y].dark_sprite
                            if block_path:
                                self._root_display.blit(dark_sprite, (put_x, put_y))
                            else:
                                self._root_display.blit(dark_sprite, (put_x, put_y))
                        else:
                            self._root_display.blit(S_FOG, (put_x, put_y))
            self._root_display.blit(e.get(DisplayComponent).sprite,
                                    ((e.get(MovementComponent).x - e.get(CameraComponent).cam_x) * TILESIZE,
                                    (e.get(MovementComponent).x - e.get(CameraComponent).cam_y) * TILESIZE))
        pygame.display.flip()
