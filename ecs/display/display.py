from ecs.display.display_component import DisplayComponent
from constants import *
from structs.game_map import GameMap
import pygame
import pysnooper


class DisplaySystem:

    def __init__(self):
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = GameMap()

    def update(self, entities):
        self._root_display.fill(BGCOLOR)
        self.map.draw_map(self._root_display, self.map.tiles)
        #for x in range(0, WIDTH, TILESIZE):
        #    pygame.draw.line(self._root_display, LIGHTGREY, (x, 0), (x, HEIGHT))
        #for y in range(0, HEIGHT, TILESIZE):
        #    pygame.draw.line(self._root_display, LIGHTGREY, (0, y), (WIDTH, y))

        for e in entities:
            dc = e.get(DisplayComponent)
            self._root_display.blit(S_PLAYER, (dc.x, dc.y))

        pygame.display.flip()
