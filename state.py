from pygame import Surface

from enums import GameState


class State:
    def selected(self, event):
        pass
    def update(self, dt: int):
        pass
    def draw(self, screen: Surface):
        pass
