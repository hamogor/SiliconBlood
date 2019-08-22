from structs.game_states import GameStates


class AiComponent:
    def __init__(self, action=None):
        self.action = action
        self.turn = GameStates.PLAYERS_TURN
