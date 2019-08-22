from ecs.action.action_component import ActionComponent
from ecs.display.display_component import DisplayComponent
from ecs.fov.fov_component import FovComponent


class ActionSystem:
    def __init__(self, level):
        self.actions = {
            "stairs": self.take_stairs,
            "move": self.move,
            "quit": self.quit
        }
        self.level = level
        self.turn_counter = 1

    def update(self, entities):
        for e in entities:
            if e.has(ActionComponent) and e.get(ActionComponent).action:
                if isinstance(e.get(ActionComponent).action, dict):
                    action, params = e.get(ActionComponent).action.popitem()
                    self.actions[action](e, params, entities)
                else:
                    action = e.get(ActionComponent).action
                    self.actions[action](e, entities)

                self.turn_counter += 1

    def move(self, entity, params, entities):
        can_move = False
        current_x, current_y = entity.get(DisplayComponent).x, entity.get(DisplayComponent).y
        direction_x, direction_y = current_x + params[0], current_y + params[1]

        if params[0] and params[1] != 0:
            if not self.level[current_x + params[0]][current_y].block_path and not self.level[current_x][current_y + params[1]].block_path:
                if not self.level[direction_x][direction_y].block_path:
                    can_move = True
        elif not self.level[direction_x][direction_y].block_path:
            can_move = True

        for e in entities:
            if e.get(DisplayComponent).x == direction_x and e.get(DisplayComponent).y == direction_y:
                can_move = False

        if can_move:
            entity.get(FovComponent).fov_recalculate = True
            entity.get(DisplayComponent).x += params[0]
            entity.get(DisplayComponent).y += params[1]
            entity.get(ActionComponent).action = None

    def take_stairs(self, entities):
        print("take stairs")
        pass

    def quit(self, entities):
        print("quit")
        pass