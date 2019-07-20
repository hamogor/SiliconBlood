from ecs.display.display_component import DisplayComponent
from ecs.keyboard.keyboard_component import KeyboardComponent
from ecs.movement.movement_component import MovementComponent
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov_component import FovComponent
from ecs.entity import Entity
from settings import *


class Player(Entity):
    def __init__(self):
        # Add components to player
        self.name = 'player'
        self.sprite = S_PLAYER
        super().__init__(DisplayComponent(self.sprite, 0, 0),
                         MovementComponent(5,5,5,5),
                         FovComponent(),
                         CameraComponent(0,0))
        self.set(KeyboardComponent(self._process_input))

    def _process_input(self, keys_pressed):
        for key_pressed in keys_pressed:
            if key_pressed in MOVE_N:
                self.get(MovementComponent).y -= 1
            elif key_pressed in MOVE_S:
                self.get(MovementComponent).y += 1
            elif key_pressed in MOVE_W:
                self.get(MovementComponent).x -= 1
            elif key_pressed in MOVE_E:
                self.get(MovementComponent).x += 1
            elif key_pressed in MOVE_NW:
                self.get(MovementComponent).x -= 1
                self.get(MovementComponent).y -= 1
            elif key_pressed in MOVE_NE:
                self.get(MovementComponent).x += 1
                self.get(MovementComponent).y -= 1
            elif key_pressed in MOVE_SW:
                self.get(MovementComponent).x -= 1
                self.get(MovementComponent).y += 1
            elif key_pressed in MOVE_SE:
                self.get(MovementComponent).x += 1
                self.get(MovementComponent).y += 1
            else:
                print("You pressed {}".format(key_pressed))