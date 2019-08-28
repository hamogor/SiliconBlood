from ecs.display.display_component import DisplayComponent
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov_component import FovComponent
from settings import WIDTH, HEIGHT, TILESIZE, GRIDHEIGHT, GRIDWIDTH, S_FOG, S_FLOOR
import pygame
import tcod


class DisplaySystem:
    def __init__(self, display, camera, level):
        self.display = display
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.empty_surface = pygame.Surface((WIDTH, HEIGHT))
        self.empty_surface.fill((0, 0, 0))
        self.camera = camera
        self.level = level
        self.player_fov = None
        self.current_frame = [[]]
        self.entity_locations = []

    def update(self, entities):
        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            if e.has(FovComponent):
                self.player_fov = e.get(FovComponent).fov_map
            if e.has(FovComponent) and e.get(FovComponent).fov_recalculate:
                self.surface.blit(self.empty_surface, (0, 0))
                for cam_x in range(0, GRIDWIDTH):
                    for cam_y in range(0, GRIDHEIGHT):
                        x, y, = self.camera.apply(cam_x, cam_y)
                        visible = tcod.map_is_in_fov(self.player_fov, x, y)
                        put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
                        try:
                            sprite = self.level[x][y].sprite
                            if visible:
                                self.surface.blit(sprite[0], (put_x, put_y))
                                self.level[x][y].explored = True

                            elif self.level[x][y].explored:
                                self.surface.blit(sprite[1], (put_x, put_y))
                            else:
                                self.surface.blit(S_FOG, (put_x, put_y))

                        except IndexError:
                            self.surface.blit(S_FOG, (put_x, put_y))

                self.draw_visible_entities(entities)
        self.display.blit(self.surface, (0, 0))

    def draw_visible_entities(self, entities):
        for e in entities:
            if self.player_fov:
                if tcod.map_is_in_fov(entities[0].get(FovComponent).fov_map, e.get(DisplayComponent).x, e.get(DisplayComponent).y):
                    self.surface.blit(e.get(DisplayComponent).sprite,
                                      ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                       (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))
                else:
                    print("dead blit")



