from ecs.action.action_component import ActionComponent
from ecs.display.display_component import DisplayComponent
from ecs.input.input_component import InputComponent
from ecs.fov.fov_component import FovComponent


# TODO - Collision, and keypress event delay for held movement.
class ActionSystem:
    def __init__(self, level):
        self.actions = {
            "move": self.move,
            "quit": self.quit
        }
        self.map = level

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
            current_x, current_y = entity.get(DisplayComponent).x, entity.get(DisplayComponent).y
            direction_x, direction_y = current_x + params[0], current_y + params[1]
            print(current_x, current_y)
            print(direction_x, direction_y)
            if not self.map[direction_x][direction_y].block_path:
                entity.get(FovComponent).fov_recalculate = True
                entity.get(DisplayComponent).x += params[0]
                entity.get(DisplayComponent).y += params[1]
                entity.get(ActionComponent).action = "none"

    def quit(self, entity):
        entity.get(InputComponent).input = False



