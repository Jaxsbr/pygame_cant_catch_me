import os
import pygame
import random
from enemy import Enemy
from events import CHANGE_STATE_EVENT, PLAYER_MOVED_EVENT
from enums import GameState, GameStatuses
from state import State
from player import Player
from tile_manager import TileManager
from tile_utils import get_surrounding_linear_indexes, get_surrounding_tile_indexes


class Game(State):

    def __init__(self) -> None:
        self._key_collected = False
        self._exit_reached = False
        self._tile_manager = TileManager()
        self._player = Player()
        self._player_move_counter = 0

        self._key_img = pygame.image.load('key.jpg')
        self._key_img = pygame.transform.scale(self._key_img, (TileManager.tile_width, TileManager.tile_height))

        self._door_img = pygame.image.load('door.jpg')
        self._door_img = pygame.transform.scale(self._door_img, (TileManager.tile_width, TileManager.tile_height))

        self._enemy_img = pygame.image.load('enemy.png')
        self._enemy_img = pygame.transform.scale(self._enemy_img, (TileManager.tile_width, TileManager.tile_height))

        self._player_img = pygame.image.load('player.png')
        self._player_img = pygame.transform.scale(self._player_img, (TileManager.tile_width, TileManager.tile_height))

        exclude_tiles_indexes = get_surrounding_tile_indexes(self._player.tile_index)

        self._key_tile_index = self._generate_random_vector2(exclude_tiles_indexes)

        exclude_tiles_indexes.append(self._key_tile_index)

        self._exit_tile_index = self._generate_random_vector2(exclude_tiles_indexes)

        exclude_tiles_indexes.append(self._exit_tile_index)

        enemy_start_tile = self._generate_random_vector2(exclude_tiles_indexes)

        self._enemy = Enemy(self._tile_manager, enemy_start_tile)

        self._key_pos = pygame.Vector2(
            self._key_tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            self._key_tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)

        self._exit_pos = pygame.Vector2(
            self._exit_tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            self._exit_tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)


    def _generate_random_vector2(self, exclude_tiles_indexes):
        # find new random vector index not in excluded list
        while True:
            x = random.randint(0, TileManager.column_count - 1)
            y = random.randint(0, TileManager.row_count - 1)

            random_vector = pygame.Vector2(x, y)

            if random_vector not in exclude_tiles_indexes:
                return random_vector


    def selected(self, event):
        self.__init__()
        print(f"game: {event}")


    def _update_game_state(self) -> bool:
        if self._exit_reached:
            self.__init__() # reset game
            pygame.event.post(
                pygame.event.Event(
                    CHANGE_STATE_EVENT,
                    {
                        "new_state": GameState.GAME_STATUS,
                        "data": GameStatuses.WIN
                    })
            )
            return True
        return False


    def _update_game_objectives(self):
        if self._player.tile_index == self._key_tile_index:
            self._key_collected = True

        if self._key_collected and self._player.tile_index == self._exit_tile_index:
            self._exit_reached = True


    def _update_enemy_player_catching(self, enemy_pos: pygame.Vector2, player_pos: pygame.Vector2):
        distance = enemy_pos.distance_to(player_pos)
        if distance <= max(TileManager.tile_width, TileManager.tile_height) + min(TileManager.tile_width, TileManager.tile_height) / 2:
            pygame.event.post(
                pygame.event.Event(
                    CHANGE_STATE_EVENT,
                    {
                        "new_state": GameState.GAME_STATUS,
                        "data": GameStatuses.LOSE
                    })
            )


    def _update_actors(self, dt):
        player_pos = self._tile_manager.get_tile_pos(self._player.tile_index)
        enemy_pos = self._tile_manager.get_tile_pos(self._enemy.tile_index)

        self._player.update(dt, player_pos)
        self._enemy.update(dt, enemy_pos, self._player.tile_index)
        self._update_enemy_player_catching(enemy_pos, player_pos)


    def _update_enemy_move_target(self):
        move_tile_indexes = get_surrounding_linear_indexes(self._enemy.tile_index)
        closest_distance = float('inf')
        closest_tile = None

        self._player_pos = self._tile_manager.get_tile_pos(self._player.tile_index)
        for index in move_tile_indexes:
            pos = self._tile_manager.get_tile_pos(index)
            distance = self._player_pos.distance_to(pos)

            if distance < closest_distance:
                closest_distance = distance
                closest_tile = index

        self._enemy.set_target(closest_tile)


    def _update_player_movements(self):
        pressed_key = pygame.key.get_pressed()

        if not self._player.is_moving() and (pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_UP] or pressed_key[pygame.K_DOWN]):
            x = 0
            if pressed_key[pygame.K_LEFT]:
                x = -1
            elif pressed_key[pygame.K_RIGHT]:
                x = 1

            y = 0
            if pressed_key[pygame.K_DOWN]:
                y = 1
            elif pressed_key[pygame.K_UP]:
                y = -1

            next_x = max(0, min(x + self._player.tile_index.x, TileManager.column_count - 1))
            next_y = max(0, min(y + self._player.tile_index.y, TileManager.row_count - 1))

            self._player.set_next_movement(pygame.Vector2(next_x, next_y))
            self._player_move_counter += 1

            if self._player_move_counter >= 2:
                self._update_enemy_move_target()
                self._player_move_counter = 0


    def update(self, dt):
        if self._update_game_state():
            return

        self._update_actors(dt)
        self._update_game_objectives()
        self._update_player_movements()


    def draw(self, screen):
        screen.fill("gray")

        self._tile_manager.draw(screen)

        if not self._key_collected:
            screen.blit(
                self._key_img,
                pygame.Rect(
                    self._key_pos.x - TileManager.tile_width_offset,
                    self._key_pos.y - TileManager.tile_height_offset,
                    TileManager.tile_width,
                    TileManager.tile_height))

        if not self._exit_reached:
            screen.blit(
                self._door_img,
                pygame.Rect(
                    self._exit_pos.x - TileManager.tile_width_offset,
                    self._exit_pos.y - TileManager.tile_height_offset,
                    TileManager.tile_width,
                    TileManager.tile_height))

            self._player.draw(screen, self._player_img)

            self._enemy.draw(screen, self._enemy_img)
