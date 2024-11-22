import random

import pygame
from tile import Tile


class TileManager:

    tile_width = 40
    tile_height = 40
    column_count = 20
    row_count = 12
    tile_width_offset = tile_width / 2
    tile_height_offset = tile_height / 2
    tile_circle_radius = min(tile_width, tile_height) / 2


    def __init__(self) -> None:
        self.tiles = [[self._create_tile(col, row) for col in range(TileManager.column_count)] for row in range(TileManager.row_count)]


    def _get_random_tile(self):
        val = random.randint(0, 10)
        tile = 0 if val > 7 else 1
        return tile


    def _create_tile(self, col, row) -> Tile:
        pos = pygame.Vector2(
            col * TileManager.tile_width + TileManager.tile_width_offset,
            row * TileManager.tile_height + TileManager.tile_height_offset)

        return Tile(
            self._get_random_tile(),
            pygame.Vector2(col, row),
            pos)


    def get_tile_pos(self, tile_index: pygame.Vector2):
        return pygame.Vector2(
            tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)


    def draw(self, screen):
       for row in range(TileManager.row_count):
            for col in range(TileManager.column_count):
                tile = self.tiles[row][col]
                color = "palegoldenrod" if tile.value == 0 else "beige"
                pygame.draw.circle(screen, color, tile.position, TileManager.tile_circle_radius)
