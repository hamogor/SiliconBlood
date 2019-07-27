from ecs.display.display_component import DisplayComponent
from ecs.keyboard.keyboard_component import KeyboardComponent
from ecs.movement.movement_component import MovementComponent
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov_component import FovComponent
from ecs.action.action_component import ActionComponent
from ecs.entity import Entity
from settings import *


class Player(Entity):
    def __init__(self, spawn_x, spawn_y):
        # Add components to player
        self.name = 'player'
        self.sprite = S_PLAYER
        self.action_to_perform = {"no_action": ""}
        super().__init__(DisplayComponent(self.sprite, 0, 0),
                         MovementComponent(spawn_x, spawn_y, spawn_x, spawn_y),
                         FovComponent(),
                         CameraComponent(0, 0),
                         ActionComponent("take_stairs"))
        self.set(KeyboardComponent(self._process_input))

    def _process_input(self, keys_pressed):
        for key_pressed in keys_pressed:
            if key_pressed in MOVE_N:
                self.get(MovementComponent).d_y -= 1
            elif key_pressed in MOVE_S:
                self.get(MovementComponent).d_y += 1
            elif key_pressed in MOVE_W:
                self.get(MovementComponent).d_x -= 1
            elif key_pressed in MOVE_E:
                self.get(MovementComponent).d_x += 1
            elif key_pressed in MOVE_NW:
                self.get(MovementComponent).d_x -= 1
                self.get(MovementComponent).d_y -= 1
            elif key_pressed in MOVE_NE:
                self.get(MovementComponent).d_x += 1
                self.get(MovementComponent).d_y -= 1
            elif key_pressed in MOVE_SW:
                self.get(MovementComponent).d_x -= 1
                self.get(MovementComponent).d_y += 1
            elif key_pressed in MOVE_SE:
                self.get(MovementComponent).d_x += 1
                self.get(MovementComponent).d_y += 1
            elif key_pressed == TAKE_STAIRS:
                self.get(ActionComponent).action_to_perform = "take_stairs"
            else:
                print("You pressed {}".format(key_pressed))
