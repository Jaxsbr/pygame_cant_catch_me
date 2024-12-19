from typing import List
import pygame


class ParticleEngine:
    def __init__(self):
        self._particles: List[Particle] = []


    def emit(self, position: pygame.Vector2, ttl: float, direction: pygame.Vector2, speed: float, size: float, color: pygame.Color, has_gravity: bool = False):
        for p in self._particles:
            if p.is_expired():
                p.reset(position, ttl, direction, speed, size, color, has_gravity)
                return p

        particle = Particle(position, ttl, direction, speed, size, color, has_gravity)
        self._particles.append(particle)
        return particle


    def reset(self):
        self._particles.clear()


    def update(self, dt):
        for p in self._particles:
            p.update(dt)


    def draw(self, screen):
        for p in self._particles:
            p.draw(screen)


class Particle:
    def __init__(self, position: pygame.Vector2, ttl: float, direction: pygame.Vector2, speed: float, size: float, color: pygame.Color, gravity: bool):
        self._position = pygame.Vector2(0, 0)
        self.reset(position, ttl, direction, speed, size, color, gravity)


    def reset(self, position: pygame.Vector2, ttl: float, direction: pygame.Vector2, speed: float, size: float, color: pygame.Color, has_gravity: bool):
        self._position.x = position.x
        self._position.y = position.y
        self._ttl = ttl
        self._original_ttl = ttl
        self._direction = direction
        self._speed = speed
        self._size = size
        self._color = pygame.Color(color.r, color.g, color.b, color.a)
        self._has_gravity = has_gravity
        self._velocity = self._direction * self._speed
        self._gravity = 9.8


    def is_expired(self):
        return self._ttl < 0


    def update(self, dt):
        if self.is_expired():
            return

        self._ttl -= 1 * dt

        if self._has_gravity:
            self._velocity.x = self._direction.x * self._speed
            self._velocity.y += self._gravity
        else:
            self._velocity = self._direction * self._speed



        self._position += self._velocity * dt

        # Calculate the opacity based on the remaining TTL
        alpha = max(0, int(255 * (self._ttl / self._original_ttl)))
        self._color.a = alpha


    def draw(self, screen):
        if self.is_expired():
            return

        # Create a temporary surface with per-pixel alpha
        circle_surface = pygame.Surface((self._size * 2, self._size * 2), pygame.SRCALPHA)
        circle_surface = circle_surface.convert_alpha()  # Ensure it supports per-pixel alpha

        # Draw the circle on the temporary surface
        pygame.draw.circle(
            circle_surface,
            self._color,
            (self._size, self._size),  # Center of the surface
            self._size
        )

        # Blit the temporary surface onto the main screen at the correct position
        screen.blit(circle_surface, (self._position.x - self._size, self._position.y - self._size))
