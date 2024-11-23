import random
from typing import List

import pygame
from game_state.tile import Tile


class TileManager:

    tile_width = 64
    tile_height = 64
    column_count = 20
    row_count = 10
    tile_width_offset = tile_width / 2
    tile_height_offset = tile_height / 2
    tile_circle_radius = min(tile_width, tile_height) / 2


    def __init__(self) -> None:
        self.tiles = [[self._create_tile(col, row) for col in range(TileManager.column_count)] for row in range(TileManager.row_count)]


    def _get_random_tile(self):
        val = random.randint(0, 17)
        if 0 <= val <= 14:
            return 1 # path
        elif val == 15:
            return 2 # holes
        elif 16 <= val <= 17:
            return 3 # trees
        else:
            print (f"unexpected value {val}")
            return 1


    def _create_tile(self, col, row) -> Tile:
        pos = pygame.Vector2(
            col * TileManager.tile_width + TileManager.tile_width_offset,
            row * TileManager.tile_height + TileManager.tile_height_offset)

        rect = pygame.Rect(
            col * TileManager.tile_width,
            row * TileManager.tile_height,
            TileManager.tile_width,
            TileManager.tile_height
        )

        return Tile(
            self._get_random_tile(),
            pygame.Vector2(col, row),
            pos,
            rect)


    def _get_color(self, val) -> str:
        if val == 1:
            return "palegoldenrod"
        elif val == 2:
            return "beige"
        else:
            return "darkgreen"


    def _is_tree(self, index) -> bool:
        if self.tiles[int(index.y)][int(index.x)].value == 3:
            return True
        return False


    def get_trees(self) -> List[pygame.Vector2]:
        trees = []
        for row in range(TileManager.row_count):
            for col in range(TileManager.column_count):
                if self.tiles[row][col].value == 3:
                    trees.append(pygame.Vector2(col, row))
        return trees


    def generate_random_vector2(self, exclude_tiles_indexes):
        while True:
            x = random.randint(0, TileManager.column_count - 1)
            y = random.randint(0, TileManager.row_count - 1)

            random_vector = pygame.Vector2(x, y)

            if random_vector not in exclude_tiles_indexes:
                return random_vector


    def get_tile_pos(self, tile_index: pygame.Vector2):
        return pygame.Vector2(
            tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)


    def draw(self, screen, tree_img):
       for row in range(TileManager.row_count):
            for col in range(TileManager.column_count):
                tile = self.tiles[row][col]
                color = self._get_color(tile.value)
                pygame.draw.circle(screen, color, tile.position, TileManager.tile_circle_radius)
                if tile.value == 3:
                    screen.blit(tree_img, tile.rect)
