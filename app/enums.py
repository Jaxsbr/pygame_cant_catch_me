from enum import Enum

class GameState(Enum):
    MENU = 1
    GAME = 2
    GAME_STATUS = 3


class GameStatuses(Enum):
    WIN = 1
    LOSE = 2
