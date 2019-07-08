from ecs.display.display_component import DisplayComponent
from ecs.input.keyboard_input_component import KeyboardInputComponent
from ecs.entity import Entity
from constants import *
import pysnooper


class Player(Entity):
    def __init__(self):
        super().__init__(DisplayComponent(S_PLAYER, 0, 0))
        self.set(KeyboardInputComponent(self._process_input))

    def _process_input(self, keys_pressed):
        for key_pressed in keys_pressed:
            if key_pressed in MOVE_N:
                self.get(DisplayComponent).y -= 1 * TILESIZE
            elif key_pressed in MOVE_S:
                self.get(DisplayComponent).y += 1 * TILESIZE
            elif key_pressed in MOVE_W:
                self.get(DisplayComponent).x -= 1 * TILESIZE
            elif key_pressed in MOVE_E:
                self.get(DisplayComponent).x += 1 * TILESIZE
            elif key_pressed in MOVE_NW:
                self.get(DisplayComponent).x -= 1 * TILESIZE
                self.get(DisplayComponent).y -= 1 * TILESIZE
            elif key_pressed in MOVE_NE:
                self.get(DisplayComponent).x += 1 * TILESIZE
                self.get(DisplayComponent).y -= 1 * TILESIZE
            elif key_pressed in MOVE_SW:
                self.get(DisplayComponent).x -= 1 * TILESIZE
                self.get(DisplayComponent).y += 1 * TILESIZE
            elif key_pressed in MOVE_SE:
                self.get(DisplayComponent).x += 1 * TILESIZE
                self.get(DisplayComponent).y += 1 * TILESIZE
            else:
                print("You pressed {}".format(key_pressed))

