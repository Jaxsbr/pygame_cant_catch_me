from dataclasses import dataclass

import pygame


@dataclass
class Tile:
    value: int
    dimentional_index: pygame.Vector2
    position: pygame.Vector2
    rect: pygame.Rect
