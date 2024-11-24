
from game_state.difficulty_engine import DifficultyEngine
from game_state.events import CHANGE_STATE_EVENT
from game_state.game import Game
import pygame

from enums import GameState
from game_status_state.game_status import GameStatus
from menu_state.menu import Menu

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.dt = 0
        self.bounds = pygame.Rect(0, 0, 1280, 640)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.bounds.width, self.bounds.height))
        self.current_state = GameState.MENU
        self.difficulty_engine = DifficultyEngine()
        self.state_objects = {
            GameState.MENU: Menu(self.bounds, self.difficulty_engine),
            GameState.GAME: Game(self._load_sprites(), self.difficulty_engine),
            GameState.GAME_STATUS: GameStatus(self.bounds)
        }


    def _load_sprites(self) -> dict[str, pygame.Surface]:
        sprite_sheet = pygame.image.load("app/img/sprite_sheet.png").convert_alpha()
        sprite_width = 64
        sprite_height = 64

        sprites = {
            "player": sprite_sheet.subsurface(pygame.Rect(0, 0, sprite_width, sprite_height)),
            "enemy": sprite_sheet.subsurface(pygame.Rect(sprite_width, 0, sprite_width, sprite_height)),
            "key": sprite_sheet.subsurface(pygame.Rect(0, sprite_height, sprite_width, sprite_height)),
            "door": sprite_sheet.subsurface(pygame.Rect(sprite_width, sprite_height, sprite_width, sprite_height)),
        }

        return sprites


    def update(self):
        self.dt = self.clock.tick(60) / 1000
        self.state_objects[self.current_state].update(self.dt)


    def draw(self):
        self.state_objects[self.current_state].draw(self.screen)
        pygame.display.flip()


    def update_game_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == CHANGE_STATE_EVENT:
                self.current_state = event.new_state
                self.state_objects[self.current_state].selected(event)
        return True


    def run_game_loop(self):
        while True:
            running = self.update_game_state()
            if not running:
                break

            self.update()
            self.draw()


if __name__ == "__main__":
    main = Main()
    main.run_game_loop()
