import pygame

from game_state.particle_trail import ParticleTrail
from game_state.tile_manager import TileManager


class Enemy:

    def __init__(self, tile_manager: TileManager, start_index: pygame.Vector2) -> None:
        self.tile_index = start_index
        self._tile_manager = tile_manager
        self._circle_radius = TileManager.tile_circle_radius / 2
        self._color = "orange"
        self._position = pygame.Vector2(0, 0)
        self._is_moving = False
        self._elapsed_move_time = 0
        self._move_time = 0.2
        self._is_caught = False
        self._draw_rect = pygame.Rect(
            self._position.x - TileManager.tile_width_offset,
            self._position.y - TileManager.tile_height_offset,
            TileManager.tile_width,
            TileManager.tile_height)
        self._particle_trail = ParticleTrail(
            [
                pygame.Color(255, 0, 0, 255),     # red
                pygame.Color(255, 255, 100, 255),   # ?
            ],
            2 # fade_time
        )


    def set_target(self, move_to_tile_index):
        self._is_moving = True
        self._move_to_tile_index = move_to_tile_index


    def is_caught_ready(self) -> bool:
        return self._is_moving and self._is_caught


    def update(self, dt, position: pygame.Vector2, player_tile_index: pygame.Vector2):
        self._position = position
        self._player_tile_index = player_tile_index

        if self._is_moving:
            self._elapsed_move_time -= dt * 1
            if self._elapsed_move_time <= 0:
                self.tile_index = self._move_to_tile_index
                self._is_moving = False

        if self._is_moving:
            self._color = "blue"
        elif self.is_caught_ready():
            self._color = "yellow"
        else:
            self._color = "orange"

        self._draw_rect.x = self._position.x - TileManager.tile_width_offset
        self._draw_rect.y = self._position.y - TileManager.tile_height_offset

        self._particle_trail.update(dt, self._position)


    def draw(self, screen, img):
        self._particle_trail.draw(screen)
        screen.blit(img, self._draw_rect)
