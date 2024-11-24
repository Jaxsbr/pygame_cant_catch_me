from game_state.difficulty_engine import DifficultyEngine
from game_state.events import CHANGE_STATE_EVENT
from enums import Difficulty, GameState
from state import State
import pygame

class Menu(State):
    def __init__(self, bounds: pygame.Rect, difficulty_engine: DifficultyEngine):
        pygame.font.init()
        self._difficulty_engine = difficulty_engine
        self._bounds = bounds
        self._button_width = 150
        self._button_height = 75
        self._easy_button = pygame.Rect(
            bounds.width / 3 - self._button_width / 2,
            bounds.height / 4 - self._button_height / 2,
            self._button_width,
            self._button_height)
        self._medium_button = pygame.Rect(
            bounds.width / 2 - self._button_width / 2,
            bounds.height / 4 - self._button_height / 2,
            self._button_width,
            self._button_height)
        self._hard_button = pygame.Rect(
            ((bounds.width / 3) * 2) - self._button_width / 2,
            bounds.height / 4 - self._button_height / 2,
            self._button_width,
            self._button_height)
        self._play_button = pygame.Rect(
            bounds.width / 2 - self._button_width / 2,
            bounds.height / 2 - self._button_height / 2,
            self._button_width,
            self._button_height)

        self._font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._hover_color = "red"
        self._text_color = "white"
        self._easy_button_hover_color = self._text_color
        self._medium_button_hover_color = self._text_color
        self._hard_button_hover_color = self._text_color
        self._play_button_hover_color = self._text_color


    def selected(self, event):
        pass


    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        self._easy_button_hover_color = self._text_color
        self._medium_button_hover_color = self._text_color
        self._hard_button_hover_color = self._text_color
        self._play_button_hover_color = self._text_color

        if self._play_button.collidepoint(mouse_pos):
            self._play_button_hover_color = self._hover_color
            if mouse_clicked:
                pygame.event.post(
                    pygame.event.Event(CHANGE_STATE_EVENT, {"new_state": GameState.GAME})
                )

        if self._easy_button.collidepoint(mouse_pos):
            self._easy_button_hover_color = self._hover_color
            if mouse_clicked:
                self._difficulty_engine.set_difficulty(Difficulty.EASY)

        if self._medium_button.collidepoint(mouse_pos):
            self._medium_button_hover_color = self._hover_color
            if mouse_clicked:
                self._difficulty_engine.set_difficulty(Difficulty.MEDIUM)

        if self._hard_button.collidepoint(mouse_pos):
            self._hard_button_hover_color = self._hover_color
            if mouse_clicked:
                self._difficulty_engine.set_difficulty(Difficulty.HARD)


    def draw(self, screen):
        screen.fill("purple")

        difficulty = self._difficulty_engine.get_difficulty()

        pygame.Surface.fill(screen, "orange" if difficulty == Difficulty.EASY else "blue", self._easy_button)
        pygame.draw.rect(screen, self._easy_button_hover_color, self._easy_button, 2)
        text_surface = self._font.render("easy", True, self._easy_button_hover_color)
        text_rect = text_surface.get_rect(center=(
            self._easy_button.x + self._button_width / 2,
            self._easy_button.y + self._button_height / 2))
        screen.blit(text_surface, text_rect)

        pygame.Surface.fill(screen, "orange" if difficulty == Difficulty.MEDIUM else "blue", self._medium_button)
        pygame.draw.rect(screen, self._medium_button_hover_color, self._medium_button, 2)
        text_surface = self._font.render("medium", True, self._medium_button_hover_color)
        text_rect = text_surface.get_rect(center=(
            self._medium_button.x + self._button_width / 2,
            self._medium_button.y + self._button_height / 2))
        screen.blit(text_surface, text_rect)

        pygame.Surface.fill(screen, "orange" if difficulty == Difficulty.HARD else "blue", self._hard_button)
        pygame.draw.rect(screen, self._hard_button_hover_color, self._hard_button, 2)
        text_surface = self._font.render("hard", True, self._hard_button_hover_color)
        text_rect = text_surface.get_rect(center=(
            self._hard_button.x + self._button_width / 2,
            self._hard_button.y + self._button_height / 2))
        screen.blit(text_surface, text_rect)

        pygame.Surface.fill(screen, "blue", self._play_button)
        pygame.draw.rect(screen, self._play_button_hover_color, self._play_button, 2)
        text_surface = self._font.render("play", True, self._play_button_hover_color)
        text_rect = text_surface.get_rect(center=(self._bounds.width / 2, self._bounds.height / 2))
        screen.blit(text_surface, text_rect)
