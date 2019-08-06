from ecs.movement.movement_component import MovementComponent
from ecs.fov.fov_component import FovComponent
from ecs.display.display_component import DisplayComponent
from settings import TILESIZE
import pygame


class MovementSystem:
    def __init__(self, level):
        self.game_map = level.level_map
        self.clock = pygame.time.Clock()

    def reset(self, level):
        self.__init__(level)

    def update(self, entities):
        for e in entities:
            self.move(e)

    def move(self, entity):
        current_x, current_y = entity.get(MovementComponent).x, entity.get(MovementComponent).y
        direction_x, direction_y = entity.get(MovementComponent).d_x, entity.get(MovementComponent).d_y
        wall = self.game_map.tiles[direction_x][direction_y].block_path

        if not wall:
            entity.get(FovComponent).fov_recalculate = True
            entity.get(MovementComponent).x = direction_x
            entity.get(MovementComponent).y = direction_y
            entity.get(DisplayComponent).x = direction_x
            entity.get(DisplayComponent).y = direction_y

        else:
            entity.get(MovementComponent).x = current_x
            entity.get(MovementComponent).y = current_y
            entity.get(MovementComponent).d_x = current_x
            entity.get(MovementComponent).d_y = current_y






