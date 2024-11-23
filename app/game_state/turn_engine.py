from enums import TurnType


class TurnEngine:
    def __init__(self):
        self._current_turn_type = TurnType.PLAYER


    def get_current_turn(self):
        return self._current_turn_type


    def next_turn(self):
        if self._current_turn_type == TurnType.PLAYER:
            self._current_turn_type = TurnType.ENEMY
        elif self._current_turn_type == TurnType.ENEMY:
            self._current_turn_type = TurnType.PLAYER
