from ecs.action.action_component import ActionComponent
from ecs.display.display_component import DisplayComponent
from ecs.input.input_component import InputComponent
from utils.map_utils import check_for_wall
from ecs.fov.fov_component import FovComponent


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

    def move_old(self, entity, params):
        if entity.get(InputComponent).input:
            current_x, current_y = entity.get(DisplayComponent).x, entity.get(DisplayComponent).y
            direction_x, direction_y = current_x + params[0], current_y + params[1]
            if not self.map[direction_x][direction_y].block_path:
                entity.get(FovComponent).fov_recalculate = True
                entity.get(DisplayComponent).x += params[0]
                entity.get(DisplayComponent).y += params[1]
                entity.get(ActionComponent).action = "none"

    def move(self, entity, params):
        can_move = False
        if entity.get(InputComponent).input:
            current_x, current_y = entity.get(DisplayComponent).x, entity.get(DisplayComponent).y
            direction_x, direction_y = current_x + params[0], current_y + params[1]
            if params[0] and params[1] != 0:
                if params == (-1, -1):  # NW
                    if not self.map[current_x][current_y - 1].block_path and not self.map[current_x - 1][current_y].block_path:
                        can_move = True
                elif params == (1, -1):  # NE
                    if not self.map[current_x][current_y - 1].block_path and not self.map[current_x + 1][current_y].block_path:
                        can_move = True
                elif params == (-1, 1):  # SW
                    if not self.map[current_x][current_y + 1].block_path and not self.map[current_x - 1][current_y].block_path:
                        can_move = True
                elif params == (1, 1):  # SE
                    if not self.map[current_x + 1][current_y].block_path and not self.map[current_x][current_y + 1].block_path:
                        can_move = True
            elif not self.map[direction_x][direction_y].block_path:
                can_move = True

            if can_move:
                entity.get(FovComponent).fov_recalculate = True
                entity.get(DisplayComponent).x += params[0]
                entity.get(DisplayComponent).y += params[1]
                entity.get(ActionComponent).action = "none"

    def quit(self, entity):
        entity.get(InputComponent).input = False



