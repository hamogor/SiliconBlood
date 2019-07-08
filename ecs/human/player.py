from ecs.display.display_component import DisplayComponent
from ecs.input.keyboard_input_component import KeyboardInputComponent
from ecs.collision.collision_component import CollisionComponent
from ecs.entity import Entity
from constants import *
import pysnooper


class Player(Entity):
    def __init__(self):
        super().__init__(DisplayComponent(S_PLAYER, 0, 0),
                         CollisionComponent(0, 0))
        self.set(KeyboardInputComponent(self._process_input))

    def _process_input(self, keys_pressed):
        for key_pressed in keys_pressed:
            if key_pressed in MOVE_N:
                self.get(CollisionComponent).y -= 1
            elif key_pressed in MOVE_S:
                self.get(CollisionComponent).y += 1
            elif key_pressed in MOVE_W:
                self.get(CollisionComponent).x -= 1
            elif key_pressed in MOVE_E:
                self.get(CollisionComponent).x += 1
            elif key_pressed in MOVE_NW:
                self.get(CollisionComponent).x -= 1
                self.get(CollisionComponent).y -= 1
            elif key_pressed in MOVE_NE:
                self.get(CollisionComponent).x += 1
                self.get(CollisionComponent).y -= 1
            elif key_pressed in MOVE_SW:
                self.get(CollisionComponent).x -= 1
                self.get(CollisionComponent).y += 1
            elif key_pressed in MOVE_SE:
                self.get(CollisionComponent).x += 1
                self.get(CollisionComponent).y += 1
            else:
                print("You pressed {}".format(key_pressed))

