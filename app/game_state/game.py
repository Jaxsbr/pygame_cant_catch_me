from game_state.difficulty_engine import DifficultyEngine
from game_state.turn_engine import TurnEngine
import pygame # type: ignore
from game_state.enemy import Enemy
from game_state.events import CHANGE_STATE_EVENT
from enums import GameState, GameStatuses, TurnType
from state import State
from game_state.player import Player
from game_state.tile_manager import TileManager
from game_state.tile_utils import get_surrounding_linear_indexes, get_surrounding_tile_indexes


class Game(State):

    def __init__(self, sprites: dict[str, pygame.Surface], difficulty_engine: DifficultyEngine) -> None:
        self._difficulty_engine = difficulty_engine
        self._key_collected = False
        self._exit_reached = False
        self._tile_manager = TileManager()
        self._tree_tiles = self._tile_manager.get_trees()
        self._player_start_tile_index = self._tile_manager.generate_random_vector2(self._tree_tiles)
        self._player = Player(self._player_start_tile_index)
        self._player_move_counter = 0
        self._has_player_moved = False
        self._enemy_move_trigger_count = self._difficulty_engine.get_enemy_move_value()
        self._sprites = sprites
        self._turn_engine = TurnEngine()

        self._tree_img = pygame.image.load('app/img/tree.png')
        self._tree_img = pygame.transform.scale(self._tree_img, (TileManager.tile_width, TileManager.tile_height))

        # tiles around player
        exclude_tiles_indexes = get_surrounding_tile_indexes(self._player.tile_index)

        # combine with trees
        exclude_tiles_indexes.extend(self._tree_tiles)

        self._key_tile_index = self._tile_manager.generate_random_vector2(exclude_tiles_indexes)

        exclude_tiles_indexes.append(self._key_tile_index)

        self._door_tile_index = self._tile_manager.generate_random_vector2(exclude_tiles_indexes)

        exclude_tiles_indexes.append(self._door_tile_index)

        enemy_start_tile = self._tile_manager.generate_random_vector2(exclude_tiles_indexes)

        self._enemy = Enemy(self._tile_manager, enemy_start_tile)

        self._key_pos = pygame.Vector2(
            self._key_tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            self._key_tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)

        self._key_rect = pygame.Rect(
            self._key_pos.x - TileManager.tile_width_offset,
            self._key_pos.y - TileManager.tile_height_offset,
            TileManager.tile_width,
            TileManager.tile_height)

        self._door_pos = pygame.Vector2(
            self._door_tile_index.x * TileManager.tile_width + TileManager.tile_width_offset,
            self._door_tile_index.y * TileManager.tile_height + TileManager.tile_height_offset)

        self._door_rect = pygame.Rect(
            self._door_pos.x - TileManager.tile_width_offset,
            self._door_pos.y - TileManager.tile_height_offset,
            TileManager.tile_width,
            TileManager.tile_height)


    def selected(self, event):
        self.__init__(self._sprites, self._difficulty_engine)
        self._player_move_counter = self._difficulty_engine.get_enemy_move_value()


    def _update_game_state(self) -> bool:
        if self._exit_reached:
            self.__init__(self._sprites, self._difficulty_engine) # reset game
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

        if self._key_collected and self._player.tile_index == self._door_tile_index:
            self._exit_reached = True


    def _update_enemy_player_catching(self, enemy_pos: pygame.Vector2, player_pos: pygame.Vector2):
        if not self._has_player_moved:
            return

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

        # Has the player stopped moving during it's turn, if yest set enemies turn
        if not self._player._is_moving and self._turn_engine.get_current_turn() == TurnType.PLAYER:
            if self._player_move_counter >= self._enemy_move_trigger_count:
                self._turn_engine.next_turn()
                self._update_enemy_move_target()
                self._player_move_counter = 0

        # Has the enemy stopped moving during it's turn, if yes set players turn
        if not self._enemy._is_moving and self._turn_engine.get_current_turn() == TurnType.ENEMY:
            self._turn_engine.next_turn()


    def _update_enemy_move_target(self):
        if not self._has_player_moved or not self._turn_engine.get_current_turn() == TurnType.ENEMY:
            return

        move_tile_indexes = get_surrounding_linear_indexes(self._enemy.tile_index)
        closest_distance = float('inf')
        closest_tile = None

        self._player_pos = self._tile_manager.get_tile_pos(self._player.tile_index)
        for index in move_tile_indexes:
            # exclude special tiles
            if index == self._key_tile_index or index == self._door_tile_index or self._tile_manager._is_tree(index):
                continue

            pos = self._tile_manager.get_tile_pos(index)
            distance = self._player_pos.distance_to(pos)

            if distance < closest_distance:
                closest_distance = distance
                closest_tile = index

        self._enemy.set_target(closest_tile)


    def _update_player_movements(self):
        if not self._turn_engine.get_current_turn() == TurnType.PLAYER:
            return

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

            next_move_tile = pygame.Vector2(
                max(0, min(x + self._player.tile_index.x, TileManager.column_count - 1)),
                max(0, min(y + self._player.tile_index.y, TileManager.row_count - 1)))

            # Can't move out of bounds
            # Can't move through door without key
            # Can't move through trees
            if next_move_tile == self._player.tile_index or (not self._key_collected and next_move_tile == self._door_tile_index) or self._tile_manager._is_tree(next_move_tile):
                return

            self._has_player_moved = True
            self._player.set_next_movement(next_move_tile)
            self._player_move_counter += 1


    def update(self, dt):
        if self._update_game_state():
            return

        self._update_actors(dt)
        self._update_game_objectives()
        self._update_player_movements()


    def draw(self, screen):
        screen.fill("gray")
        self._tile_manager.draw(screen, self._tree_img)

        if not self._key_collected:
            screen.blit(self._sprites["key"], self._key_rect)

        if not self._exit_reached:
            screen.blit(self._sprites["door"],self._door_rect)
            self._player.draw(screen, self._sprites["player"],)
            self._enemy.draw(screen, self._sprites["enemy"],)
