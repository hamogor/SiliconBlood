from ecs.display.display_component import DisplayComponent
from ecs.keyboard.keyboard_component import KeyboardComponent
from ecs.movement.movement_component import MovementComponent
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov_component import FovComponent
from ecs.action.action_component import ActionComponent
from ecs.entity import Entity
from settings import *
import pygame


class Actor(Entity, pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, sprite, name):
        # Add components to player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.name = 'player'
        self.sprite = sprite

