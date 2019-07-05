from constants import WIDTH, HEIGHT, BGCOLOR
from ecs.display_component import DisplayComponent
import pygame


class DisplaySystem:

    def __init__(self):
        self._root_display = pygame.display.set_mode((WIDTH, HEIGHT))

    def update(self, entities):
        self._root_display.fill(BGCOLOR)

        for e in entities:
            dc = e.get(DisplayComponent)
            self._root_display.blit(dc.x, dc.y, dc.sprite, dc.colour)

        pygame.display.flip()
