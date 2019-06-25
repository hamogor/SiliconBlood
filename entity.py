from map_objects.game_map import GameMap


class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def perform_action(self, action, game_map):
        if action.get('move'):
            self.move(action.get('move'), game_map)

    def move(self, directions, game_map):
        dx, dy = directions

        if not game_map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
