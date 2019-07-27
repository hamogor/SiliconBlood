from ecs.action.action_component import ActionComponent
from ecs.movement.movement_component import MovementComponent


class ActionSystem:
    actions = {}

    def __init__(self, level):
        self.level = level
        self.actions = {
            "take_stairs": self.take_stairs
        }



    def update(self, entities):
        for e in entities:
            if e.has(ActionComponent):
                if e.get(ActionComponent).action_to_perform:
                    action = getattr(e.get(ActionComponent), "action_to_perform")
                    if self.actions[action]:
                        self.actions[action](e)
                        e.get(ActionComponent).action_to_perform = None

    def take_stairs(self, entity):
        if entity.has(MovementComponent):
            entity_x = entity.get(MovementComponent).x
            entity_y = entity.get(MovementComponent).y
        if self.level.level_map.tiles[entity_x][entity_y].name == "stairs":
            print("on stairs")