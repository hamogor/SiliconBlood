from ecs.collision.collision_component import CollisionComponent
from ecs.display.display_component import DisplayComponent
from constants import *
import pysnooper


class CollisionSystem:
    def __init__(self, game_map):
        self.game_map = game_map

    def update(self, entities):
        for e in entities:
            cur_x = e.get(DisplayComponent).x
            cur_y = e.get(DisplayComponent).y

            d_x = e.get(CollisionComponent).x
            d_y = e.get(CollisionComponent).y

            if not self.game_map[d_x][d_y].block_path:
                e.get(DisplayComponent).x = d_x * TILESIZE
                e.get(DisplayComponent).y = d_y * TILESIZE
            else:
                e.get(DisplayComponent).x = cur_x
                e.get(DisplayComponent).y = cur_y
                e.get(CollisionComponent).x = int(cur_x / TILESIZE)
                e.get(CollisionComponent).y = int(cur_y / TILESIZE)
