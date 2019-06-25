class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def perform_action(self, action):
        if action.get('move'):
            self.move(action.get('move'))

    def move(self, directions):
        dx, dy = directions
        self.x += dx
        self.y += dy
