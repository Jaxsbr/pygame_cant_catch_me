
from events import CHANGE_STATE_EVENT
from game import Game
import pygame

from enums import GameState
from game_status import GameStatus
from menu import Menu

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.dt = 0
        self.bounds = pygame.Rect(0, 0, 800, 480)
        self.current_state = GameState.MENU
        self.state_objects = {
            GameState.MENU: Menu(self.bounds),
            GameState.GAME: Game(),
            GameState.GAME_STATUS: GameStatus(self.bounds)
        }
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.bounds.width, self.bounds.height))


    def update(self):
        self.dt = self.clock.tick(60) / 1000
        self.state_objects[self.current_state].update(self.dt)


    def draw(self):
        self.state_objects[self.current_state].draw(self.screen)
        pygame.display.flip()


    def update_game_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quit")
                return False
            elif event.type == CHANGE_STATE_EVENT:
                print(f"eventZ: {event}")
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
