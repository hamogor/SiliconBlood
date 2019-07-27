class ActionComponent:
    def __init__(self, *actions):
        self.actions = [action for action in actions]
        self.action_to_perform = None
