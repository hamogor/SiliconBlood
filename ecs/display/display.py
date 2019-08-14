from ecs.display.display_component import DisplayComponent
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov_component import FovComponent
from ecs.camera.camera import CameraSystem
from settings import *
import pygame
import tcod


# TODO - Proper tile blitting (from pygame)
# TODO - only reblit tile if its moved
class DisplaySystem:
    def __init__(self, level_map, display):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display = display
        self.map = level_map
        self.camera = CameraSystem()

    def update(self, entities):
        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            if e.has(FovComponent) and e.get(FovComponent).fov_recalculate:
                for cam_x in range(0, GRIDWIDTH):
                    for cam_y in range(0, GRIDHEIGHT):
                        x, y, = self.camera.apply(cam_x, cam_y)
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
                        try:
                            sprite = self.map[x][y].sprite
                            block_path = self.map[x][y].block_path

                            if visible:
                                # Assign tiles correct sprite based on block_path value and just blit each tile
                                if block_path:
                                    self.surface.blit(sprite[0], (put_x, put_y))
                                else:
                                    self.surface.blit(sprite[0], (put_x, put_y))
                                self.map[x][y].explored = True
                            elif self.map[x][y].explored:
                                if self.map[x][y].block_path:
                                    self.surface.blit(sprite[1], (put_x, put_y))
                                else:
                                    self.surface.blit(sprite[1], (put_x, put_y))
                            else:
                                self.surface.blit(S_FOG, (put_x, put_y))
                        except IndexError:
                            self.surface.blit(S_FOG, (put_x, put_y))
                        if e.has(DisplayComponent):
                            # This is broken
                            self.surface.blit(e.get(DisplayComponent).sprite,
                                                    ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                                     (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

        self.display.blit(self.surface, (0, 0))
        pygame.display.update()


