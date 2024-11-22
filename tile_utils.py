from typing import List
import pygame

from tile_manager import TileManager


def get_surrounding_linear_indexes(current_index: pygame.Vector2) -> List[pygame.Vector2]:
    indexes = []
    indexes.append(pygame.Vector2(current_index.x, current_index.y - 1)) # up
    indexes.append(pygame.Vector2(current_index.x - 1, current_index.y)) # left
    indexes.append(pygame.Vector2(current_index.x + 1, current_index.y)) # right
    indexes.append(pygame.Vector2(current_index.x, current_index.y + 1)) # down

    # only return indexes that are within the tiles array bounds
    filtered_tile_indexes = [
        index for index in indexes
        if 0 <= index.x < TileManager.column_count and 0 <= index.y < TileManager.row_count
    ]

    return filtered_tile_indexes


def get_surrounding_tile_indexes(current_index: pygame.Vector2) -> List[pygame.Vector2]:
    indexes = []
    indexes.append(pygame.Vector2(current_index.x - 1, current_index.y - 1))
    indexes.append(pygame.Vector2(current_index.x, current_index.y - 1))
    indexes.append(pygame.Vector2(current_index.x + 1, current_index.y - 1))
    indexes.append(pygame.Vector2(current_index.x - 1, current_index.y))
    indexes.append(pygame.Vector2(current_index.x, current_index.y))
    indexes.append(pygame.Vector2(current_index.x + 1, current_index.y))
    indexes.append(pygame.Vector2(current_index.x - 1, current_index.y + 1))
    indexes.append(pygame.Vector2(current_index.x, current_index.y + 1))
    indexes.append(pygame.Vector2(current_index.x + 1, current_index.y + 1))

    # only return indexes that are within the tiles array bounds
    filtered_tile_indexes = [
        index for index in indexes
        if 0 <= index.x < TileManager.column_count and 0 <= index.y < TileManager.row_count
    ]

    return filtered_tile_indexes
