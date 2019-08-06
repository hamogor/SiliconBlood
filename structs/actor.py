from ecs.display.display_component import DisplayComponent
from ecs.entity import Entity
from settings import *
import pygame


class Actor(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite.convert()
        super().__init__(DisplayComponent(x, y, self.image))
        self.rect = self.image.get_rect()
