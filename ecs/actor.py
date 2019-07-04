import constants
import math
import pygame
import constants as const


class ObjActor:
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x  # map address
        self.y = y  # map address
        self.name_object = name_object
        self.sprite = sprite
        self.vx = 0
        self.vy = 0

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def get_keys(self):
        self.vx, self.xy = 0, 0
        keys = pygame.key.get_pressed()
        if constants.MOVE_W in keys:
            self.vx = - const.PLAYER_SPEED
        elif constants.MOVE_E in keys:
            self.vx = const.PLAYER_SPEED
        elif constants.MOVE_N in keys:
            self.vy = - const.PLAYER_SPEED
        elif constants.MOVE_S in keys:
            self.vy = const.PLAYER_SPEED

    def draw(self, surface_main):
        surface_main.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy, game_map, game_objects):
        tile_is_wall = game_map.tiles[self.x + dx][self.y + dy].block_path
        self.get_keys()

        target = None

        for object in game_objects:
            if (object is not self and
                    object.x == self.x + dx and
                    object.y == self.y + dy and
                    object.creature):

                target = object
                break

        if target:
            print(self.creature.name_instance + " attacks " + target.creature.name_instance)
            target.creature.take_damage(5)

        if not tile_is_wall and target is None:
            self.x += dx
            self.y += dy


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
