from ecs.display.display_component import DisplayComponent
from ecs.camera.camera_component import CameraComponent
from settings import *
import pygame
import time


class DisplaySystem:
    def __init__(self, map, camera):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = map
        self.camera = camera

    def update(self, entities):

        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            self.surface.blit(S_WALL, (0, 0))
            self.surface.fill(BLACK)
            for cam_x in range(MAPWIDTH):
                for cam_y in range(MAPHEIGHT):
                    x, y, = self.camera.apply(cam_x, cam_y)
                    print(x, y)
                    try:
                        if self.map[x][y].block_path:
                            self.surface.blit(S_WALL, (x * 32, y * 32))
                        else:
                            self.surface.blit(S_FLOOR, (x * 32, y * 32))
                    except IndexError:
                        pass
                    if e.has(DisplayComponent):
                        self.surface.blit(e.get(DisplayComponent).sprite,
                                          (e.get(DisplayComponent).x,
                                           e.get(DisplayComponent).y))

        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()


