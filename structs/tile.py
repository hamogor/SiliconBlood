from ecs.entity import Entity
import pygame


class StrucTile(pygame.Surface, Entity):
    def __init__(self, block_path, block_sight, sprite=None, dark_sprite=None, name=""):
        self.name = name
        self.block_path = block_path
        self.block_sight = block_sight
        self.sprite = sprite
        self.dark_sprite = dark_sprite
        self.explored = False
        #self.rect = sheet.get_rect()

        # Give the tile an animation component
        #if self.rect:
        #    super().__init__(AnimationComponent(sheet, cols, rows))
