from ecs.display.display_component import DisplayComponent
from settings import *
import pygame
import time


class DisplaySystem:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

    def update(self, entities):

        for e in entities:
            self.surface.fill(BLACK)
            for x in range(MAPWIDTH):
                for y in range(MAPHEIGHT):
                    if e.has(DisplayComponent):
                        self.surface.blit(e.get(DisplayComponent).sprite,
                                          (e.get(DisplayComponent).x,
                                           e.get(DisplayComponent).y))
        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()


