import pygame

from game_state.particle_trail import ParticleTrail
from game_state.tile_manager import TileManager

class Player:

    def __init__(self, start_tile_index) -> None:
        self.tile_index = start_tile_index
        self.next_move_tile = pygame.Vector2(0, 0)
        self._color = "red"
        self._is_moving = False
        self._elapsed_move_time = 0
        self._move_time = 0.2
        self._circle_radius = TileManager.tile_circle_radius / 2
        self._position = pygame.Vector2(0, 0)
        self._draw_rect = pygame.Rect(
            self._position.x - TileManager.tile_width_offset,
            self._position.y - TileManager.tile_height_offset,
            TileManager.tile_width,
            TileManager.tile_height)
        self._particle_trail = ParticleTrail(
            [
                pygame.Color(255, 255, 0, 255),   # yellow
                pygame.Color(255, 255, 255, 255),   # ?
            ],
            2 # fade_time
        )


    def set_next_movement(self, move_tile: pygame.Vector2):
        self._is_moving = True
        self._elapsed_move_time = self._move_time
        self.next_move_tile = move_tile


    def is_moving(self) -> bool:
        return self._is_moving


    def _update_movement(self, dt):
        if self._is_moving:
            self._elapsed_move_time -= dt * 1
            if self._elapsed_move_time <= 0:
                self.tile_index = self.next_move_tile
                self._is_moving = False


    def update(self, dt, position) -> None:
        self._position = position
        self._update_movement(dt)
        self._particle_trail.update(dt, self._position)

        if self._is_moving:
            self._color = "blue"
        else:
            self._color = "red"

        self._draw_rect.x = self._position.x - TileManager.tile_width_offset
        self._draw_rect.y = self._position.y - TileManager.tile_height_offset


    def draw(self, screen, img) -> None:
        self._particle_trail.draw(screen)
        screen.blit(img, self._draw_rect)
