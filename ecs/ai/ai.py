from ecs.ai.ai_component import AiComponent
from ecs.action.action_component import ActionComponent
from ecs.display.display_component import DisplayComponent
from structs.game_states import GameStates
import math
import tcod


class AiSystem:
    def __init__(self, level):
        self.player = None
        self.level = level

    def update(self, entities):
        for e in entities:
            if e.name == "player":
                self.player = e
            if e.has(AiComponent) and e.has(ActionComponent):
                if e.get(AiComponent).turn == GameStates.ENEMY_TURN:
                    self.move_towards(e)

                    e.get(AiComponent).turn = GameStates.PLAYERS_TURN

    def move_towards(self, entity):
        dx = self.player.get(DisplayComponent).x - entity.get(DisplayComponent).x
        dy = self.player.get(DisplayComponent).y - entity.get(DisplayComponent).y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        entity.get(ActionComponent).action = {"move": (dx, dy)}

