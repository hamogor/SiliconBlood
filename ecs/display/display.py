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
        self.map = GameMap(generate=True)
        self.camera = GameMap()
        self.fov_map = tcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        self.width = WIDTH
        self.height = HEIGHT

    def update(self, entities):
        for e in entities:
            # get map top left corner offset from the game map
            map_off_x, map_off_y = get_map_offset(e)

            # get our map display offset from the console top left corner
            con_off_x, con_off_y = get_console_offset(e)

            for y in range(min(self.camera.height, self.map.height)):
                for x in range(min(self.camera.width, self.map.width))
                map_x = x + map_off_x
                map_y = y + map_off_y
                cam_x = x + cam_off_x * TILESIZE
                cam_y = y + cam_off_y * TILESIZE
                visible = tcod.map_is_in_fov(e.get(FovComponent), map_x, map_y)
                wall = self.map.tiles[map_x][map_y].block_sight
                if visible:
                    if wall:
                        self._root_display.blit(S_WALL, (cam_x, cam_y))
                    else:
                        self._root_display.blit(S_FLOOR, (cam_x, cam_y))
                    self.map.tiles[map_x][map_y].explored = True
                elif self.map.tiles[map_x][map_y].explored:
                    if wall:
                        self._root_display.blit(S_DWALL, (cam_x, cam_y))
                    else:
                        self._root_display.blit(S_DFLOOR, (cam_x, cam_y))
                else:
                    self._root_display.blit(LIGHT_GREY, (cam_x, cam_y))
            self._root_display.blit(S_PLAYER, (1024, 1024))

        pygame.display.flip()

    def get_map_offset(self, e):
        player_x = int(e.get(DisplayComponent).x / TILESIZE)
        player_y = int(e.get(DisplayComponent).y / TILESIZE)

        map_x = int(player_x - self.camera.width / 2)
        if map_x < 0:
            map_x = 0
        elif map_x + self.camera.width > self.map.width:
            map_x = self.map.width - self.camera.width
        
        map_y = int(player_y - self.camera.height / 2)
        if map_y < 0:
            map_y = 0
        elif map_y + self.camera.height > self.map.height:
            map_y = self.map.height - self.camera.height

        return map_x, map_y

    def get_camera_offset(e):
        cam_x = int((self.camera.width - self.map.width) / 2)
        cam_y = int((self.camera.height - self.map.height) / 2)
        if cam_x < 0:
            cam_x = 0
        if cam_y < 0:
            cam_y = 0

        return cam_x, cam_y
