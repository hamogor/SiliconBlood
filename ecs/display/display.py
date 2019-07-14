from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent
from ecs.movement.movement_component import MovementComponent
from constants import *
from structs.game_map import GameMap
import pygame
import tcod
import pysnooper


class DisplaySystem:

    def __init__(self):
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = GameMap()
        self.camera = Camera(WIDTH, HEIGHT)
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        self.width = WIDTH
        self.height = HEIGHT

    def update(self, entities):
        for e in entities:
            if e.get(FovComponent).fov_recalculate:
                dc = e.get(DisplayComponent)
                for x in range(e.get(MovementComponent).x - int(GRIDWIDTH / 2), e.get(MovementComponent).x + int(GRIDWIDTH / 2)):
                    for y in range(e.get(MovementComponent).y - int(GRIDHEIGHT / 2), e.get(MovementComponent).y + int(GRIDHEIGHT / 2)):
                        self._root_display.blit(S_PLAYER, self.camera.apply())



    #def update(self, entities):
    #    for e in entities:
    #        if e.get(FovComponent).fov_recalculate:
    #            dc = e.get(DisplayComponent)
    #            for x in range(e.get(MovementComponent).x - int(GRIDWIDTH / 2), e.get(MovementComponent).x + int(GRIDWIDTH / 2)):
    #                for y in range(e.get(MovementComponent).y - int(GRIDHEIGHT / 2), e.get(MovementComponent).y + int(GRIDHEIGHT / 2)):
    #                    visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
    #                    self._root_display.blit(S_FOG, (x * TILESIZE, y * TILESIZE))
    #                    if visible:
    #                        if self.map.tiles[x][y].block_path:
    #                            self._root_display.blit(S_WALL, (x * TILESIZE, y * TILESIZE))
    #                        else:
    #                            self._root_display.blit(S_FLOOR, (x * TILESIZE, y * TILESIZE))
    #                        self.map.tiles[x][y].explored = True
    #                    elif self.map.tiles[x][y].explored:
    #                        if self.map.tiles[x][y].block_path:
    #                            self._root_display.blit(S_DWALL, (x * TILESIZE, y * TILESIZE))
    #                        else:
    #                            self._root_display.blit(S_DFLOOR, (x * TILESIZE, y * TILESIZE))
    #            self._root_display.blit(S_PLAYER, (dc.x, dc.y))
    #    pygame.display.flip()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

