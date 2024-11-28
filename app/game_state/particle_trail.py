import math
import random
from typing import List
import pygame

from particle_engine import ParticleEngine

class ParticleTrail:

    def __init__(self, colors: List[pygame.Color], fade_time: float) -> None:
        self._fade_time = fade_time
        self._emit_count = 0.1
        self._elapsed_emit = self._emit_count
        self._particle_count = 1
        self._particle_engine = ParticleEngine()
        self._colors = colors

    def update(self, dt, position: pygame.Vector2):
        self._position = position
        self._particle_engine.update(dt)

        self._elapsed_emit -= dt * 1
        if self._elapsed_emit <= 0:
            self._elapsed_emit = self._emit_count
            for i in range(self._particle_count):
                angle = random.choice(range(0, 361, 6))
                radians = math.radians(angle)
                self._particle_engine.emit(
                    self._position,
                    self._fade_time,
                    pygame.Vector2(math.cos(radians), math.sin(radians)),
                    random.choice([2]),
                    random.choice([5, 7]),
                    random.choice(self._colors),
                    False
                )


    def draw(self, screen) -> None:
        self._particle_engine.draw(screen)
