from ecs.input.input_component import InputComponent
from ecs.display.display_component import DisplayComponent
from ecs.entity import Entity
from settings import *
import pygame


class Actor(Entity, pygame.sprite.Sprite):
    def __init__(self, *components):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*components)
