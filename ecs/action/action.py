from ecs.action.action_component import ActionComponent
from ecs.display.display_component import DisplayComponent
from ecs.input.input_component import InputComponent
from settings import TILESIZE, PLAYER_SPEED
import pygame


class ActionSystem:
    def __init__(self):
        self.actions = {
            "move": self.move,
            "quit": self.quit
        }

    def update(self, entities):
        for e in entities:
            if e.has(ActionComponent):
                if e.get(ActionComponent).action:
                    try:
                        action = getattr(e.get(ActionComponent), "action")
                        if self.actions[action[0]]:
                            self.actions[action[0]](e, action[1] if action[1] else None)
                    except KeyError:
                        pass

    def move(self, entity, params):
        if entity.get(InputComponent).input:
            entity.get(DisplayComponent).x += params[0] * TILESIZE
            entity.get(DisplayComponent).y += params[1] * TILESIZE
            entity.get(InputComponent).input = False

    def quit(self, entity):
        entity.get(InputComponent).input = False



