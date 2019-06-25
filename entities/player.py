import tcod as tcod


class Player:
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self.exit_signal = False

    def perform_action(self, action):
        if action.get('move'):
            self.move(action.get('move'))
        if action.get('exit'):
            self.exit()

    def move(self, move):
        dx, dy = move
        self.x += dx
        self.y += dy

    def exit(self):
        self.exit_signal = True
        return True


