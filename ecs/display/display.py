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
        self.world_map = pygame.Surface((WIDTH, HEIGHT))
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
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        self._root_display.blit(S_FOG, (x * TILESIZE, y * TILESIZE))
                        if visible:
                            if self.map.tiles[x][y].block_path:
                                self._root_display.blit(S_WALL, self.camera.apply(e))
                            else:
                                self._root_display.blit(S_FLOOR, self.camera.apply(e))
                            self.map.tiles[x][y].explored = True
                        elif self.map.tiles[x][y].explored:
                            if self.map.tiles[x][y].block_path:
                                self._root_display.blit(S_DWALL, self.camera.apply(e))
                            else:
                                self._root_display.blit(S_DFLOOR, self.camera.apply(e))
                self._root_display.blit(S_PLAYER, self.camera.apply(e))
        pygame.display.flip()

    def update(self, entities):
        for e in entities:
            map_x, map_y = self.get_map_offset(e)
            for con_y in range(min(HEIGHT, self.map.height)):  # Probably doesn't have these attributes
                for con_x in range(min(WIDTH, self.map.width)): #probably just use len
                    x = con_x + map_x
                    y = con_y + map_y
                    visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, x)
                    wall = self.map[x][y].block_path
                    if visible:
                        if wall:
                            self._root_display.blit(S_WALL, con_x, con_y)
                        else:
                            self._root_display.blit(S_FLOOR, con_x, con_y)
                        self.map.tiles[x][y].explored = True
                    elif self.map.tiles[x][y].explored:
                        if wall:
                            self._root_display.blit(S_DWALL, con_x, con_y)
                        else:
                            self._root_display.blit(S_DFLOOR, con_x, con_y)
                    else:
                        self._root_display.blit(S_FOG, con_x, con_y)
        pygame.display.flip()

    def get_map_offset(e):
        map_x = int(e.get(DisplayComponent).x - WIDTH / 2)
        if map_x < 0:
            map_x = 0
        elif map_x + WIDTH > self.world_map.width:
            map_x = self.world_map.width - WIDTH
        
        map_y = int(e.get(DisplayComponent).y - HEIGHT / 2)
        if map_y > 0:
            map_y = 0
        elif map_y + HEIGHT > self.world_map.height:
            map_y = self.world_map.height - HEIGHT

        return (map_x, map_y)

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
