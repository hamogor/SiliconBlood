from settings import WIDTH, HEIGHT, TILESIZE, S_FOG, GRIDWIDTH, GRIDHEIGHT
from ecs.fov.fov_component import FovComponent
from ecs.movement.movement_component import MovementComponent
from ecs.display.display_component import DisplayComponent
import pygame
import tcod


class DisplaySystem:
    __slots__ = ['level', 'camera', 'map', '_root_display', 'display']

    def __init__(self, level, camera, display):
        self.map = level.level_map
        self.display = display
        self.camera = camera
        self._root_display = pygame.Surface((WIDTH, HEIGHT))

    def reset(self, level):
        self.__init__(level, self.camera, self.display)

    def update(self, entities):
        for e in entities:
            self.camera.update(e)
            if e.get(FovComponent).fov_recalculate:
                for cam_y in range(0, GRIDWIDTH):
                    for cam_x in range(0, GRIDHEIGHT):
                        x, y = self.camera.apply(cam_x, cam_y)
                        try:
                            block_path = self.map.tiles[x][y].block_path
                            sprite = self.map.tiles[x][y].sprite
                        except IndexError:
                            continue
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        put_x, put_y = cam_x * TILESIZE, cam_y * TILESIZE
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
                                    ((e.get(DisplayComponent).x - self.camera.x) * TILESIZE,
                                    (e.get(DisplayComponent).y - self.camera.y) * TILESIZE))
            self.display.blit(self._root_display, (0, 0))
            pygame.display.flip()
