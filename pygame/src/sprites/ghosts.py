"""
This module handles ghosts
A single ghost class responsible for rending ghost,
ghost manager class responsible for creating multiple ghost objects aka ghosts
ghose movement class responsible for moving the ghost with lerp
GhostManager takes ghost matrix pos, grid start pos, matrix, game state object.
Ghost takes name, ghost matrix pos, grid start pos, matrix and game state object
Ghost movement class should need ghost coordinate pos, matrix, game state, some more parameters.
"""
from abc import abstractmethod, ABC

from pygame.sprite import Sprite
from pygame import Surface
from pygame import image, transform
import pygame.time as pytime
from pygame.time import wait
from pygame.rect import Rect

import random

from src.game.state_management import GameState
from src.sprites.sprite_configs import GHOST_PATHS
from src.configs import PACMAN, CELL_SIZE, GHOST_DELAYS, GHOST_SCATTER_TARGETS, GHOST_POINT
from src.utils.coord_utils import get_coords_from_idx, get_idx_from_coords
from src.utils.ghost_movement_utils import get_direction, get_is_intersection, get_is_move_valid
from src.sounds import SoundManager

from src.log_handle import get_logger
logger = get_logger(__name__)

class Ghost(Sprite, ABC):
    def __init__(self,
                 name: str,
                 ghost_matrix_pos: tuple[int, int],
                 grid_start_pos: tuple[int | float, int | float],
                 matrix: list[list[str]],
                 game_state: GameState
                 ):
        super().__init__()
        self.name = name
        self._ghost_matrix_pos = ghost_matrix_pos
        self._grid_start_pos = grid_start_pos
        self._matrix = matrix
        self.num_rows = len(self._matrix)
        self.num_cols = len(self._matrix[0])
        self._game_state = game_state
        self._is_released = False
        self._creation_time = pytime.get_ticks()
        self._dead_wait = GHOST_DELAYS[self.name]
        self.move_direction_mapper = {"up": (-1, 0), "down":(2, 0), 
                                      "right": (0, 2), "left": (0, -1)}
        self.prev_pos = None
        self._t = 0
        self._accelerate = 0.2
        self._direction = None
        self._target = None
        self.prev = None
        self.next_tile = None
        self._direction_prevent = {(-1, 0): (1, 0), (1, 0): (-1, 0),
                                     (0, 1): (0, -1), (0, -1): (0, 1)}
        self.is_scared = False
        self.curr_pos = None
        self.release_time = None
        self.sounds = SoundManager()
        self.load_images()

    def _get_coords_from_idx(self, p1):
        return get_coords_from_idx(p1, *self._grid_start_pos, 
                                   *CELL_SIZE, self.num_rows, self.num_cols)
    
    def _get_idx_from_coords(self, p1):
        return get_idx_from_coords(*p1,
                                   *self._grid_start_pos, CELL_SIZE[0])
    
    def build_bounding_boxes(self, x, y):
        self.rect.x = x + (CELL_SIZE[0] * 2 - self.rect.width) // 2
        self.rect.y = y + (CELL_SIZE[1] * 2 - self.rect.height) // 2

    def load_images(self):
        ghost_images = GHOST_PATHS[self.name][0]
        blue_images = GHOST_PATHS['blue'][0]
        self.normal_image = transform.scale(image.load(ghost_images).convert_alpha(),
                                     PACMAN)
        self.blue_image = transform.scale(image.load(blue_images).convert_alpha(),
                                     PACMAN)
        self.image = self.normal_image
        x, y = self._get_coords_from_idx(self._ghost_matrix_pos)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect_x = x
        self.rect_y = y

    def lerp(self, source, dest):
        x1, y1 = source
        x2, y2 = dest
        if self._target is None or self._t == 1:
            return x1, y1
        if self._t < 1:
            self._t += self._accelerate
        else:
            self._t = 1  

        x = (1 - self._t) * x1 + self._t * x2
        y = (1 - self._t) * y1 + self._t * y2
        return x, y
    
    def check_is_released(self):
        if self._is_released:
            return
        curr_time = pytime.get_ticks()
        if (curr_time - self._creation_time) > self._dead_wait:
            self._is_released = True
            self._dead_wait = 1500
            self.rect_x, self.rect_y = self._get_coords_from_idx((11, self._ghost_matrix_pos[1]))
            self.release_time = pytime.get_ticks()

    def move_ghost(self):
        if not self._is_released:
            return
        if self._target is None:
            self.prepare_movement()
        source = self._get_coords_from_idx(self.prev)
        dest = self._get_coords_from_idx(self.next_tile)
        self.rect_x, self.rect_y = self.lerp(source, dest)
        curr_mat_x, curr_mat_y = self._get_idx_from_coords((self.rect_x, self.rect_y))
        if self.name == 'blinky':
            self._game_state.blinky_matrix_pos = (curr_mat_x, curr_mat_y)
        self.curr_pos = (curr_mat_x, curr_mat_y)
        if (self._t == 1) \
            or (self.rect_x == dest[0] and self.rect_y == dest[1]):
            check_prev = self._direction_prevent.get(self._direction)
            prev_val = self._get_direction_reverse_map(check_prev)
            if get_is_intersection(self.next_tile, self._matrix, 
                                   prev_val):
                
                self.prepare_movement()
            else:
                if not get_is_move_valid(self.next_tile, 
                                         self._get_direction_reverse_map(self._direction), 
                                         self._matrix):
                    self.prepare_movement()
                else:
                    self.prev = self.next_tile
                    self.next_tile = (self.next_tile[0] + self._direction[0],
                                  self.next_tile[1] + self._direction[1])
                
                self._t = 0
    
    def _get_direction_reverse_map(self, direction):
        match direction:
            case (-1, 0):
                return 'up'
            case (1, 0):
                return "down"
            case (0, -1):
                return "left"
            case(0, 1):
                return "right"
      
    def _boundary_check(self):
        if not self.next_tile:
            return
        if (self.next_tile[1] >= self.num_cols):
            self.next_tile = (self.next_tile[0], 0)
            return
        if self.next_tile[1] < 0:
            self.next_tile = (self.next_tile[0], self.num_cols - 1)

    def prepare_movement(self):
        ghost_x, ghost_y = self._get_idx_from_coords((self.rect_x, self.rect_y))
        if self.next_tile:
            ghost_x, ghost_y = self.next_tile
        if self.is_scared:
            self._target = self.get_random_target()
        else:
            self._target = self.determine_target()
        prev = self._direction_prevent.get(self._direction)
        self._direction = get_direction((ghost_x, ghost_y),
                                        self._target, 
                                        self._matrix, 
                                        prev
                                        )
        self._t = 0
        self.next_tile = (ghost_x + self._direction[0], 
                          ghost_y + self._direction[1])
        self.prev = (ghost_x, ghost_y)

    @abstractmethod
    def determine_target(self):
        ...
        
    def get_target_pacman_dir(self, pacman_rect: tuple, 
                              pacman_dir: tuple,
                              look_ahead: int=4):
        match pacman_dir:
            case "l":
                target = (pacman_rect[0], pacman_rect[1] - look_ahead)
                if target[1] < 0:
                    target = (pacman_rect[0], self.num_cols - look_ahead - 1)
                return target
            
            case "r":
                target = (pacman_rect[0], pacman_rect[1] + look_ahead)
                if target[1] > self.num_cols:
                    target = (pacman_rect[0], 0)
                return target
            case "u":
                return (pacman_rect[0] - look_ahead, pacman_rect[1])
            case "d":
                return (pacman_rect[0] + look_ahead, pacman_rect[1])
            case _:
                return pacman_rect

    def get_random_target(self):
        rand_row = random.randrange(0, self.num_rows)
        rand_col = random.randrange(0, self.num_cols)
        return rand_row, rand_col
    
    def make_ghost_scared(self):
        self._direction = self._direction_prevent[self._direction]
        self.is_scared = True
        self.prepare_movement()

    def check_if_pacman_powered(self):
        if not self._is_released:
            if self.image != self.normal_image:
                self.image = self.normal_image
            return
        if self._game_state.power_event_trigger_time is not None and \
                self.release_time > self._game_state.power_event_trigger_time:
            return
        if self._game_state.is_pacman_powered:
            if self.image != self.blue_image:
                self.image = self.blue_image
                self.make_ghost_scared()
        else:
            if self.image != self.normal_image:
                self.image = self.normal_image
                self.is_scared = False

    def reset_ghost(self):
        self._t = 0
        self._direction = None
        self._target = None
        self._curr_pos = None
        self.prev = None
        self.next_tile = None
        self.release_time = None
        self.is_scared = False
        self.rect.x
        x, y = self._get_coords_from_idx(self._ghost_matrix_pos)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect_x = x
        self.rect_y = y
        self._is_released = False
        self._creation_time = pytime.get_ticks()

    def check_collisions(self):
        ghost_rect = Rect(self.rect.x, self.rect.y, 
                          PACMAN[0]//2, PACMAN[1]//2)
        pacman_coords = (self._game_state.pacman_rect[0],
                         self._game_state.pacman_rect[1],
                         self._game_state.pacman_rect[2]//2,
                         self._game_state.pacman_rect[3]//2)
        pacman_rect = Rect(pacman_coords)
        if ghost_rect.colliderect(pacman_rect):
            if self.is_scared:
                self.reset_ghost()  
                self.sounds.play_sound("eat_ghost")
                self._game_state.points += GHOST_POINT
            else:
                self._game_state.is_pacman_dead = True
                self.sounds.play_sound("death")
                wait(1000)

    def update(self, dt):
        self.build_bounding_boxes(self.rect_x, self.rect_y)
        self.check_is_released()
        self._boundary_check()
        self.move_ghost()
        self.check_if_pacman_powered()
        self.check_collisions()

class Blinky(Ghost):
    def determine_target(self):
        mode = self._game_state.ghost_mode
        match mode:
            case "scatter":
                target = GHOST_SCATTER_TARGETS[self.name]
            case "chase":
                pacman_rect = self._game_state.pacman_rect
                target = self._get_idx_from_coords((pacman_rect[0], pacman_rect[1]))
        return target
    
class Pinky(Ghost):
    def calculate_pacman_direction(self):
        pacman_dir = self._game_state.pacman_direction
        pacman_rect = self._game_state.pacman_rect
        pacman_rect = self._get_idx_from_coords((pacman_rect[0], 
                                                        pacman_rect[1]))
        return self.get_target_pacman_dir(pacman_rect, 
                                          pacman_dir,
                                          )

    def determine_target(self):
        mode = self._game_state.ghost_mode
        match mode:
            case "scatter":
                return GHOST_SCATTER_TARGETS[self.name]
            case "chase":
                return self.calculate_pacman_direction()
            
class Inky(Ghost):
    def calculate_inky_target(self):
        pacman_rect = self._game_state.pacman_rect
        pacman_rect = self._get_idx_from_coords((pacman_rect[0], pacman_rect[1]))
        pacman_dir = self._game_state.pacman_direction
        blinky_cell = self._game_state.blinky_matrix_pos
        inky_pacman_target = self.get_target_pacman_dir(pacman_rect,
                                                        pacman_dir,
                                                        2)
        vec_row = inky_pacman_target[0] - blinky_cell[0]
        vec_col = inky_pacman_target[1] - blinky_cell[1]
        target_row = blinky_cell[0] + vec_row * 2
        target_col = blinky_cell[1] + vec_col * 2
        return target_row, target_col  

    def determine_target(self):
        mode = self._game_state.ghost_mode
        match mode:
            case "scatter":
                return GHOST_SCATTER_TARGETS[self.name]
            case "chase":
                return self.calculate_inky_target()
            
class Clyde(Ghost):
    def get_clyde_random_target(self):
        pacman_rect = self._game_state.pacman_rect
        pacman_rect = self._get_idx_from_coords((pacman_rect[0], pacman_rect[1]))
        if not self.curr_pos:
            return pacman_rect
        dis = abs(pacman_rect[0] - self.curr_pos[0]) + abs(pacman_rect[1] - self.curr_pos[1])
        if dis > 8:
            return self.get_random_target()
        return pacman_rect
        
    def determine_target(self):
        mode = self._game_state.ghost_mode
        match mode:
            case "scatter":
                return GHOST_SCATTER_TARGETS[self.name]
            case "chase":
                return self.get_clyde_random_target()

class GhostManager:
    def __init__(self,
                 screen: Surface,
                 game_state: GameState,
                 matrix: list[list[str]],
                 ghost_matrix_pos: tuple[int, int],
                 grid_start_pos: tuple[int, int],
                 ):
        self.screen = screen
        self.game_state = game_state
        self.matrix = matrix
        self.ghost_matrix_pos = ghost_matrix_pos
        self.grid_start_pos = grid_start_pos
        self.ghosts_list = []
        self.load_ghosts()
    
    def load_ghosts(self):
        # ghost_pos = self.ghost_matrix_pos
        adder = 0
        ghosts = [('blinky', Blinky), 
                  ('pinky', Pinky), 
                  ('inky', Inky), 
                  ('clyde', Clyde)]
        for ghost_name, ghost in ghosts:
            ghost_pos = (self.ghost_matrix_pos[0], self.ghost_matrix_pos[1] + adder)
            self.ghosts_list.append(ghost(ghost_name,
                                          ghost_pos,
                                          self.grid_start_pos,
                                          self.matrix,
                                          self.game_state))
            adder += 1