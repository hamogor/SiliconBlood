import pygame
from ecs.entity import Entity


class Actor(Entity, pygame.sprite.Sprite):
    def __init__(self, *components, name=None):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*components)
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.name = name
        self.blocks = True
