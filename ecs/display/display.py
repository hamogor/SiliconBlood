from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent
from ecs.movement.movement_component import MovementComponent
from structs.game_map import GameMap
from constants import *
import pygame
import tcod
import pysnooper


class DisplaySystem:

    def __init__(self):
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = GameMap(generate=True)

    def update(self, entities):
        for e in entities:
            map_off_x, map_off_y = self.get_map_offset(e)
            cam_off_x, cam_off_y = self.get_console_offset(e)
            if e.get(FovComponent).fov_recalculate:
                for y in range(min(CAM_HEIGHT, self.map.height)):
                    for x in range(min(CAM_WIDTH, self.map.width)):
                        map_x = x + map_off_x
                        map_y = y + map_off_y
                        cam_x = x + cam_off_x
                        cam_y = y + cam_off_y
                        visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                        if visible:
                            if self.map.tiles[map_x][map_y].block_path:
                                self._root_display.blit(S_WALL, (cam_x * TILESIZE, cam_y * TILESIZE))
                            else:
                                self._root_display.blit(S_FLOOR, (cam_x * TILESIZE, cam_y * TILESIZE))
                            self.map.tiles[cam_x][cam_y].explored = True
                        elif self.map.tiles[map_x][map_y].explored:
                            if self.map.tiles[cam_x][cam_y].block_path:
                                self._root_display.blit(S_DWALL, (cam_x * TILESIZE, cam_y * TILESIZE))
                            else:
                                self._root_display.blit(S_DFLOOR, (cam_x * TILESIZE, cam_y * TILESIZE))
                self._root_display.blit(S_PLAYER, (14 * TILESIZE, 10 * TILESIZE))
            print(e.get(MovementComponent).x)
            print(e.get(MovementComponent).y)
        pygame.display.flip()

    @pysnooper.snoop()
    def get_map_offset(self, entity):
        # get our map panel's top left corner offset from the actual game map
        map_x = int(entity.get(MovementComponent).x - self.map.width / 2)
        if map_x + CAM_WIDTH > self.map.width:
            map_x = self.map.width - CAM_WIDTH
        map_y = int(entity.get(MovementComponent).y - CAM_HEIGHT / 2)
        if map_y + CAM_HEIGHT > self.map.height:
            map_y = self.map.height - CAM_HEIGHT

        return map_x, map_y

    @pysnooper.snoop()
    def get_console_offset(self, entity):
        # get our map's display offset from the top left corner of the console
        con_x = int((CAM_WIDTH - self.map.width) / 2)
        con_y = int((CAM_HEIGHT - self.map.height) / 2)

        return con_x, con_y
