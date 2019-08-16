from ecs.action.action_component import ActionComponent
from ecs.display.display_component import DisplayComponent
from ecs.input.input_component import InputComponent
from utils.map_utils import check_for_corner_movement
from ecs.fov.fov_component import FovComponent


class ActionSystem:
    def __init__(self, level):
        self.actions = {
            "stairs": self.take_stairs,
            "move": self.move,
            "quit": self.quit,
        }
        self.level = level

    def reset(self, level):
        self.__init__(level)

    def update(self, entities):
        # Send actions as dictionaries instead
        for e in entities:
            if e.has(ActionComponent):
                if e.get(ActionComponent).action:
                    try:
                        action = getattr(e.get(ActionComponent), "action")
                        print(action)
                        if self.actions[action[0]]:
                            self.actions[action[0]](e, action[1] if action[1] else None)
                    except KeyError:
                        print("keyerror")

                        pass

    def move(self, entity, params):
        can_move = False
        if entity.get(InputComponent).input:
            current_x, current_y = entity.get(DisplayComponent).x, entity.get(DisplayComponent).y
            direction_x, direction_y = current_x + params[0], current_y + params[1]
            if params[0] and params[1] != 0:
                if check_for_corner_movement(current_x, current_y, params, self.level.tiles):
                    if not self.level.tiles[direction_x][direction_y].block_path:
                        can_move = True
            elif not self.level.tiles[direction_x][direction_y].block_path:
                can_move = True

            if can_move:
                entity.get(FovComponent).fov_recalculate = True
                entity.get(DisplayComponent).x += params[0]
                entity.get(DisplayComponent).y += params[1]
                entity.get(ActionComponent).action = None
                print("north: {}".format(
                    self.level.tiles[entity.get(DisplayComponent).x][
                        entity.get(DisplayComponent).y - 1].assignment))
                print("south: {}".format(
                    self.level.tiles[entity.get(DisplayComponent).x][
                        entity.get(DisplayComponent).y + 1].assignment))
                print("west: {}".format(
                    self.level.tiles[entity.get(DisplayComponent).x - 1][
                        entity.get(DisplayComponent).y].assignment))
                print("east: {}".format(
                    self.level.tiles[entity.get(DisplayComponent).x + 1][
                        entity.get(DisplayComponent).y].assignment))
                print("NE: {}".format(self.level.tiles[entity.get(DisplayComponent).x + 1][
                                          entity.get(DisplayComponent).y - 1].assignment))
                print("NW: {}".format(self.level.tiles[entity.get(DisplayComponent).x - 1][
                                          entity.get(DisplayComponent).y - 1].assignment))
                print("SE: {}".format(self.level.tiles[entity.get(DisplayComponent).x + 1][
                                          entity.get(DisplayComponent).y + 1].assignment))
                print("SW: {}".format(self.level.tiles[entity.get(DisplayComponent).x - 1][
                                          entity.get(DisplayComponent).y + 1].assignment))

    def take_stairs(self, entity):
        print("called")
        if entity.has(DisplayComponent):
            entity_x = entity.get(DisplayComponent).x
            entity_y = entity.get(DisplayComponent).y
            if self.level.tiles[entity_x][entity_y].name == "stairs":
                self.level.generate_next_level()
        entity.get(ActionComponent).action = None

    def quit(self, entity):
        entity.get(InputComponent).input = False



