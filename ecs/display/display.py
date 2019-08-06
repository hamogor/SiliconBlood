from ecs.display.display_component import DisplayComponent
from settings import *
import pygame


class DisplaySystem:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

    def update(self, entities):
        for e in entities:
            if e.has(DisplayComponent):
                self.display.blit(e.get(DisplayComponent).sprite,
                                  (e.get(DisplayComponent).x,
                                   e.get(DisplayComponent).y))
        pygame.display.flip()

