from enums import Difficulty


class DifficultyEngine:
    def __init__(self) -> None:
        self._current_difficulty = Difficulty.EASY


    def set_difficulty(self, difficulty: Difficulty):
        self._current_difficulty = difficulty


    def get_difficulty(self) -> Difficulty:
        return self._current_difficulty


    def get_enemy_move_value(self) -> int:
        if self._current_difficulty == Difficulty.EASY:
            return 3
        elif self._current_difficulty == Difficulty.MEDIUM:
            return 2
        elif self._current_difficulty == Difficulty.HARD:
            return 1

        print(f"unexpected difficulte: {self._current_difficulty}")
        return 3
