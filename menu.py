from events import CHANGE_STATE_EVENT
from enums import GameState
from state import State
import pygame

class Menu(State):
    def __init__(self, bounds: pygame.Rect):
        pygame.font.init()
        self._bounds = bounds
        self._button_width = 100
        self._button_height = 75
        self._play_button = pygame.Rect(
            bounds.width / 2 - self._button_width / 2,
            bounds.height / 2 - self._button_height / 2,
            self._button_width,
            self._button_height)
        self._font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._hover_color = "white"


    def selected(self, event):
        print(f"menu: {event}")


    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if self._play_button.collidepoint(mouse_pos):
            self._hover_color = "yellow"
            if mouse_clicked:
                pygame.event.post(
                    pygame.event.Event(CHANGE_STATE_EVENT, {"new_state": GameState.GAME})
                )
        else:
            self._hover_color = "white"


    def draw(self, screen):
        screen.fill("purple")
        pygame.Surface.fill(screen, "blue", self._play_button)
        pygame.draw.rect(screen, self._hover_color, self._play_button, 2)

        text_surface = self._font.render("play", True, self._hover_color)
        text_rect = text_surface.get_rect(center=(self._bounds.width / 2, self._bounds.height / 2))
        screen.blit(text_surface, text_rect)
