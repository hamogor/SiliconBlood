import pygame
from structs.actor import Actor
from ecs.entity import Entity


class Player(Actor, Entity, pygame.sprite.Sprite):
    def __init__(self, *components, name=None):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*components, name="player")
