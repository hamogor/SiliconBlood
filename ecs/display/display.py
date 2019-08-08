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
    def __init__(self, level_map):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = level_map
        self.camera = CameraSystem()

    def update(self, entities):

        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            self.display.fill(BLACK)
            for cam_x in range(GRIDWIDTH):
                for cam_y in range(GRIDHEIGHT):
                    x, y, = self.camera.apply(cam_x, cam_y)
                    visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                    put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
                    try:
                        sprite = self.map[x][y].sprite
                        if visible:
                            # Assign tiles correct sprite based on block_path value and just blit each tile
                            if self.map[x][y].block_path:
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
                        pass
                    if e.has(DisplayComponent):
                        # This is broken
                        self.surface.blit(e.get(DisplayComponent).sprite,
                                                ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                                 (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()


