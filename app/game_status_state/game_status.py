from game_state.difficulty_engine import DifficultyEngine
from game_state.events import CHANGE_STATE_EVENT
from enums import GameState, GameStatuses
from state import State
import pygame

class GameStatus(State):
    def __init__(self, bounds: pygame.Rect):
        pygame.font.init()
        self._bounds = bounds
        self._button_width = 200
        self._button_height = 125
        self._status_button = pygame.Rect(
            bounds.width / 2 - self._button_width / 2,
            bounds.height / 2 - self._button_height,
            self._button_width,
            self._button_height)
        self._play_button = pygame.Rect(
            ((bounds.width / 3) * 2) - self._button_width / 2,
            bounds.height / 2,
            self._button_width,
            self._button_height)
        self._menu_button = pygame.Rect(
            bounds.width / 3 - self._button_width / 2,
            bounds.height / 2,
            self._button_width,
            self._button_height)
        self._font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._hover_color = "red"
        self._text_color = "white"
        self._menu_button_hover_color = self._text_color
        self._play_button_hover_color = self._text_color


    def selected(self, event):
        self._status = event.data
        if self._status == GameStatuses.WIN:
            self._fill_color = "green"
            self._status_text = "you win"
        elif self._status == GameStatuses.LOSE:
            self._fill_color = "salmon"
            self._status_text = "you lose"


    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        self._play_button_hover_color = self._text_color
        self._menu_button_hover_color = self._text_color

        if self._play_button.collidepoint(mouse_pos):
            self._play_button_hover_color = self._hover_color
            if mouse_clicked:
                pygame.event.post(
                    pygame.event.Event(CHANGE_STATE_EVENT, {"new_state": GameState.GAME})
                )

        if self._menu_button.collidepoint(mouse_pos):
            self._menu_button_hover_color = self._hover_color
            if mouse_clicked:
                pygame.event.post(
                    pygame.event.Event(CHANGE_STATE_EVENT, {"new_state": GameState.MENU})
                )


    def draw(self, screen):
        screen.fill(self._fill_color)

        # Status Button
        pygame.Surface.fill(screen, "blue", self._status_button)
        pygame.draw.rect(screen, "white", self._status_button, 2)
        text_surface = self._font.render(self._status_text, True, "white")
        text_rect = text_surface.get_rect(
            center=(
                self._status_button.x + self._button_width / 2,
                self._status_button.y + self._button_height / 2))
        screen.blit(text_surface, text_rect)

        # Play Button
        pygame.Surface.fill(screen, "blue", self._play_button)
        pygame.draw.rect(screen, self._play_button_hover_color, self._play_button, 2)
        text_surface = self._font.render("play again", True, self._play_button_hover_color)
        text_rect = text_surface.get_rect(
            center=(
                self._play_button.x + self._button_width / 2,
                self._play_button.y + self._button_height / 2))
        screen.blit(text_surface, text_rect)

        pygame.Surface.fill(screen, "blue", self._menu_button)
        pygame.draw.rect(screen, self._menu_button_hover_color, self._menu_button, 2)
        text_surface = self._font.render("menu", True, self._menu_button_hover_color)
        text_rect = text_surface.get_rect(
            center=(
                self._menu_button.x + self._button_width / 2,
                self._menu_button.y + self._button_height / 2))
        screen.blit(text_surface, text_rect)
