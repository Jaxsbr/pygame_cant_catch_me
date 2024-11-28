import pygame

from game_state.tile_manager import TileManager


class Key:
    def __init__(self, tile_index: pygame.Vector2) -> None:
        self.tile_index = tile_index
        self.position = pygame.Vector2(
            tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)

        self._rect = pygame.Rect(
            self.position.x - TileManager.tile_width_offset,
            self.position.y - TileManager.tile_height_offset,
            TileManager.tile_width,
            TileManager.tile_height)


    def match_key_location(self, tile_index) -> bool:
        return self.tile_index == tile_index


    def draw(self, screen, img: pygame.Surface):
        screen.blit(img, self._rect)
