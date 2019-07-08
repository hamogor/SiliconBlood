from ecs.collision.collision_component import CollisionComponent
from ecs.display.display_component import DisplayComponent
from constants import *
import pysnooper


class CollisionSystem:
    def __init__(self, game_map):
        self.game_map = game_map

    def update(self, entities):
        for e in entities:
            c_collision = e.get(CollisionComponent)
            if not self.game_map[c_collision.x][c_collision.y].block_path:
                e.get(DisplayComponent).x = c_collision.x * TILESIZE
                e.get(DisplayComponent).y = c_collision.y * TILESIZE
            else:
                pass
# 320 display y
# 288 display x
# 9 collision x
# 10 collision y
#
#
# 320
# 288
# 11
# 10
