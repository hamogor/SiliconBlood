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

    def update(self, entities):
        for e in entities:
            map_x, map_y = self.get_map_offset(e)
            for con_y in range(min(HEIGHT, self.map.height)):
                for con_x in range(min(WIDTH, self.map.width)):
                    x = con_x + int(map_x / TILESIZE)
                    y = con_y + int(map_y / TILESIZE)
                    visible = tcod.map_is_in_fov(e.get(FovComponent).fov_map, x, y)
                    wall = self.map.tiles[x][y].block_path
                    if visible:
                        if wall:
                            self._root_display.blit(S_WALL, (con_x * TILESIZE, con_y * TILESIZE))
                        else:
                            self._root_display.blit(S_FLOOR, (con_x * TILESIZE, con_y * TILESIZE))
                        self.map.tiles[x][y].explored = True
                    elif self.map.tiles[x][y].explored:
                        if wall:
                            self._root_display.blit(S_DWALL, (con_x * TILESIZE, con_y * TILESIZE))
                        else:
                            self._root_display.blit(S_DFLOOR, (con_x * TILESIZE, con_y * TILESIZE))
            self._root_display.blit(S_PLAYER, (14 * TILESIZE, 10 * TILESIZE))
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
