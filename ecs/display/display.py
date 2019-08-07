from ecs.display.display_component import DisplayComponent
from ecs.camera.camera_component import CameraComponent
from ecs.camera.camera import CameraSystem
from settings import *
import pygame
import time


class DisplaySystem:
    def __init__(self, map):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = map
        self.camera = CameraSystem()

    def update(self, entities):

        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            self.surface.fill(BLACK)
            for cam_x in range(MAPWIDTH):
                for cam_y in range(MAPHEIGHT):
                    x, y, = self.camera.apply(cam_x, cam_y)
                    put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
                    try:
                        if self.map[x][y].block_path:
                            self.surface.blit(S_WALL, (put_x, put_y))
                        else:
                            self.surface.blit(S_FLOOR, (put_x, put_y))
                    except IndexError:
                        pass
                    if e.has(DisplayComponent):
                        # This is broken
                        self.surface.blit(e.get(DisplayComponent).sprite,
                                                ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                                 (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()


