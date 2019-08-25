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
        self.camera = camera
        self.level = level
        self.player_fov = None
        self.current_frame = [[]]

    def update(self, entities):
        #self.surface.fill((0, 0, 0))
        for e in entities:
            if e.has(CameraComponent):
                self.camera.update(e)
            if e.has(FovComponent) and e.get(FovComponent).fov_recalculate:
                self.player_fov = e.get(FovComponent).fov_map
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

            if e.has(DisplayComponent) and e.name != "player":
                    self.draw_entity(e)
            elif e.has(DisplayComponent) and e.name == "player" and e.has(FovComponent) and e.get(FovComponent).fov_map:
                self.surface.blit(e.get(DisplayComponent).sprite,
                                  ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                   (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

            #self.clear_entities(entities)
            #self.draw_entities(entities)
        self.display.blit(self.surface, (0, 0))
        pygame.display.update()

    def draw_entities(self, entities):
        for e in entities:
            if tcod.map_is_in_fov(self.player_fov, e.get(DisplayComponent).x, e.get(DisplayComponent).y):
                self.surface.blit(e.get(DisplayComponent).sprite,
                                  ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                   (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

    def draw_entity(self, e):
        if tcod.map_is_in_fov(self.player_fov, e.get(DisplayComponent).x, e.get(DisplayComponent).y):
            self.surface.blit(e.get(DisplayComponent).sprite,
                              ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                               (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

    def clear_entities(self, entities):
        for e in entities:
            clear_rec = pygame.Surface((TILESIZE, TILESIZE))#
            self.surface.blit(clear_rec,
                              ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                               (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))

