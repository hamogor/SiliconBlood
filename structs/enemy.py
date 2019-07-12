from ecs.display.display_component import DisplayComponent
from ecs.input.keyboard_input_component import KeyboardInputComponent
from ecs.movement.movement_component import MovementComponent
from ecs.fov.fov_component import FovComponent
from ecs.entity import Entity
from constants import *


class Enemy(Entity):
    def __init__(self):
        super().__init__(DisplayComponent(S_ENEMY, 15 * TILESIZE, 15 * TILESIZE),
                         MovementComponent(0, 0),
                         FovComponent())

