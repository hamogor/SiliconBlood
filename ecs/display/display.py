from ecs.display.display_component import DisplayComponent
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov_component import FovComponent
from ecs.camera.camera import CameraSystem
from settings import *
import pygame
import tcod
from pprint import pprint as pp


# TODO - Proper tile blitting (from pygame)
# TODO - only reblit tile if its moved
class DisplaySystem:
    def __init__(self, level_map, display):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display = display
        self.map = level_map.tiles
        self.camera = CameraSystem()
        self.fov = None

    def reset(self, level_map):
        self.__init__(level_map, self.display)

    def update(self, entities):
        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            if e.has(FovComponent) and e.get(FovComponent).fov_recalculate:
                self.fov = e.get(FovComponent).fov_map
                for cam_x in range(0, GRIDWIDTH):
                    for cam_y in range(0, GRIDHEIGHT):
                        x, y, = self.camera.apply(cam_x, cam_y)
                        visible = tcod.map_is_in_fov(self.fov, x, y)
                        put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
                        try:
                            sprite = self.map[x][y].sprite
                            if visible:
                                self.surface.blit(sprite[0], (put_x, put_y))
                                self.map[x][y].explored = True
                            elif self.map[x][y].explored:
                                self.surface.blit(sprite[1], (put_x, put_y))
                            else:
                                self.surface.blit(S_FOG, (put_x, put_y))
                        except IndexError:
                            self.surface.blit(S_FOG, (put_x, put_y))

            if e.has(DisplayComponent) and e.name != "player":
                self.draw_entity(e)
            elif e.has(DisplayComponent) and e.name == "player":
                self.surface.blit(e.get(DisplayComponent).sprite,
                                  ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                   (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()

    def draw_entity(self, e):
        if tcod.map_is_in_fov(self.fov, e.get(DisplayComponent).x, e.get(DisplayComponent).y):
            self.surface.blit(e.get(DisplayComponent).sprite,
                              ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                               (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))




