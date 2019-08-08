from settings import *
from ecs.input.input_component import InputComponent
from ecs.action.action_component import ActionComponent
import pygame


class InputSystem:
    def __init__(self):
        self.keys_pressed = []

    def update(self, entities):

        for e in entities:
            if e.has(InputComponent):

                for event in pygame.event.get():
                    print(event)
                    if event.type == pygame.QUIT:
                        e.get(ActionComponent).action = "quit"
                    if event.type == pygame.KEYDOWN:
                        e.get(InputComponent).input = True
                        if event.key in MOVE_W:
                            e.get(ActionComponent).action = ("move", (-1, 0))
                        elif event.key in MOVE_E:
                            e.get(ActionComponent).action = ("move", (1, 0))
                        elif event.key in MOVE_N:
                            e.get(ActionComponent).action = ("move", (0, -1))
                        elif event.key in MOVE_S:
                            e.get(ActionComponent).action = ("move", (0, 1))
                        elif event.key in MOVE_NW:
                            e.get(ActionComponent).action = ("move", (-1, -1))
                        elif event.key in MOVE_NE:
                            e.get(ActionComponent).action = ("move", (1, -1))
                        elif event.key in MOVE_SW:
                            e.get(ActionComponent).action = ("move", (-1, 1))
                        elif event.key in MOVE_SE:
                            e.get(ActionComponent).action = ("move", (1, 1))
                        elif event.key == pygame.K_ESCAPE:
                            e.get(ActionComponent).action = "quit"
                    elif event.type == pygame.KEYUP:
                        e.get(InputComponent).input = False
                        e.get(ActionComponent).action = "none"



