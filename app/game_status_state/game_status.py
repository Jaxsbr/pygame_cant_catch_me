import math
import random
from particle_engine import ParticleEngine
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
            bounds.height / 3 - self._button_height,
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
        self._message_font = pygame.font.Font(pygame.font.get_default_font(), 60)
        self._font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._hover_color = "red"
        self._text_color = "white"
        self._menu_button_hover_color = self._text_color
        self._play_button_hover_color = self._text_color
        self._emit_count = 0.5
        self._elapsed_emit_count = 0
        self._particle_pos = pygame.Vector2(
            self._status_button.x + self._button_width / 2,
            self._status_button.y + self._button_height / 2
        )
        self._particle_engine = ParticleEngine()
        self._happy_colors = [
            pygame.Color(255, 255, 0, 255),   # yellow
            pygame.Color(255, 0, 0, 255),     # red
            pygame.Color(128, 0, 128, 255),   # purple
            pygame.Color(0, 0, 255, 255),     # blue
            pygame.Color(0, 255, 0, 255),   # green
            pygame.Color(173, 216, 230, 255),   # light blue
            pygame.Color(255, 192, 203, 255),   # pink
            pygame.Color(255, 165, 0, 255),   # orange
        ]
        self._sad_colors = [
            pygame.Color(128, 128, 128, 255),   # gray
            pygame.Color(0, 0, 0, 255),     # black
        ]


    def selected(self, event):
        self._status = event.data
        if self._status == GameStatuses.WIN:
            self._fill_color = "green"
            self._status_text = "YOU WIN"
        elif self._status == GameStatuses.LOSE:
            self._fill_color = "salmon"
            self._status_text = "YOU LOSE"

        self._particle_engine.reset()


    def _update_particles(self, dt):
        self._particle_engine.update(dt)

        self._elapsed_emit_count += 1 * dt
        if self._elapsed_emit_count >= self._emit_count:
            self._elapsed_emit_count = 0

            # TODO:
            # Calculate ttl based on speed
            # e.g. higher speed expires faster as it leaves the screen quicker

            if self._status == GameStatuses.WIN:
                particle_count = random.randint(7, 20)
                for i in range(particle_count):
                    angle = random.choice(range(0, 361, 6))
                    radians = math.radians(angle)
                    self._particle_engine.emit(
                        self._particle_pos,
                        random.choice([1.5, 3, 4.5]),
                        pygame.Vector2(math.cos(radians), math.sin(radians)),
                        random.choice([100, 250, 300, 500, 600]),
                        random.choice([5, 7, 9, 12, 25]),
                        random.choice(self._happy_colors),
                        True
                    )
            else:
                particle_count = random.randint(1, 2)
                for i in range(particle_count):
                    angle = random.choice(range(0, 361, 6))
                    radians = math.radians(angle)
                    self._particle_engine.emit(
                        self._particle_pos,
                        random.choice([1.5, 3]),
                        pygame.Vector2(math.cos(radians), math.sin(radians)),
                        random.choice([50, 100]),
                        random.choice([9, 12]),
                        random.choice(self._sad_colors),
                        False
                    )


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

        self._update_particles(dt)


    def draw(self, screen):
        screen.fill(self._fill_color)

        self._particle_engine.draw(screen)

        # Status
        text_surface = self._message_font.render(self._status_text, True, "white")
        text_surface_shadow = self._message_font.render(self._status_text, True, "gray")
        text_rect = text_surface.get_rect(
            center=(
                self._status_button.x + self._button_width / 2,
                self._status_button.y + self._button_height / 2))
        text_shadow_rect = text_surface.get_rect(
            center=(
                self._status_button.x + self._button_width / 2 + 1.5,
                self._status_button.y + self._button_height / 2 + 1.5))
        screen.blit(text_surface_shadow, text_shadow_rect)
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
