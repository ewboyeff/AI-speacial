from math import ceil

from pygame import image, transform
from pygame.sprite import Sprite
from pygame import Surface, USEREVENT
from pygame.time import set_timer, get_ticks

from src.configs import CELL_SIZE, PACMAN_SPEED, PACMAN, DOT_POINT, POWER_POINT
from src.game.state_management import GameState
from src.sprites.sprite_configs import *
from src.utils.coord_utils import (get_coords_from_idx, 
                                   get_idx_from_coords, 
                                   get_tiny_matrix,
                                   precompute_matrix_coords)
from src.sounds import SoundManager
from src.log_handle import get_logger
logger = get_logger(__name__)

class Pacman(Sprite):
    def __init__(self, 
                 screen: Surface, 
                 game_state: GameState, 
                 matrix: list[list[str]],
                 pacman_pos: tuple,
                 start_pos: tuple):
        super().__init__()
        self.screen = screen
        self.game_state = game_state
        self.pacman_pos = pacman_pos
        self.matrix = matrix
        self.start_pos = start_pos
        self.load_all_frames()
        self.calculate_pacman_coords()
        self.load_image()
        self.calculate_tiny_matrix()
        self.calculate_coord_matrix()
        self.frame_delay = 5
        self.sound = SoundManager()
        self.collectibles = self.count_dots_powers()

    def count_dots_powers(self):
        collectibles = 0
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                if col + 1 >= len(self.matrix[0]):
                    continue
                if self.matrix[row][col] in ['dot', 'power'] and \
                        self.matrix[row+1][col] not in ['wall', 'elec', 'null']:
                    collectibles += 1
        # logger.info("total_collectibles: %s",collectibles)
        return collectibles

    def load_image(self):
        self.image = self.frames[self.curr_frame_idx]
        self.rect_x = self.pacman_x_coord
        self.rect_y = self.pacman_y_coord
        self.rect = self.image.get_rect(topleft=(self.pacman_x_coord,
                                                 self.pacman_y_coord))
    
    def build_bounding_boxes(self, x: int | float, y: int | float):
        self.rect.x = x + (CELL_SIZE[0] * 2 - self.rect.width) // 2
        self.rect.y = y + (CELL_SIZE[1] * 2 - self.rect.height) // 2
        
    def frame_update(self):
        self.frame_delay -= 1
        if self.frame_delay <= 0:
            self.frame_delay = 5
            self.curr_frame_idx = (self.curr_frame_idx + 1) % len(self.frames)
            self.image = self.frames[self.curr_frame_idx]

    def frame_direction_update(self):
        if self.move_direction != "":
            self.frames = self.direction_mapper[self.move_direction]

    def calculate_pacman_coords(self):
        x, y = get_coords_from_idx(
            self.pacman_pos,
            self.start_pos[0],
            self.start_pos[1],
            CELL_SIZE[0],
            CELL_SIZE[1],
            len(self.matrix),
            len(self.matrix[0])
        )
        self.pacman_x_coord = x
        self.pacman_y_coord = y
    
    def load_all_frames(self):
        def frame_helper(direction):
            width, height = PACMAN
            return [
                transform.scale(image.load(path).convert_alpha(), (width, height))
                for path in PACMAN_PATHS[direction]
            ]
        self.curr_frame_idx = 0
        self.left_frames = frame_helper("left")
        self.right_frames = frame_helper("right")
        self.down_frames = frame_helper("down")
        self.up_frames = frame_helper("up")
        self.direction_mapper = {
            "l": self.left_frames,
            "r": self.right_frames,
            "u": self.up_frames,
            "d": self.down_frames,
        }
        self.frames = self.right_frames
        self.move_direction = self.game_state.direction

    def calculate_tiny_matrix(self):
        self.tiny_matrix = get_tiny_matrix(self.matrix,
                                           CELL_SIZE[0],
                                           PACMAN_SPEED)
        self.subdiv = CELL_SIZE[0] // PACMAN_SPEED
        self.tiny_start_x = self.pacman_pos[0] * self.subdiv
        self.tiny_start_y = self.pacman_pos[1] * self.subdiv

    def calculate_coord_matrix(self):
        self.coord_matrix = precompute_matrix_coords(*self.start_pos,
                                                     PACMAN_SPEED,
                                                     len(self.tiny_matrix),
                                                     len(self.tiny_matrix[0]))

    def edges_helper_vertical(self, row: int, 
                              col: int, 
                              additive: int):
        for r in range(self.subdiv * 2):
            if self.tiny_matrix[row + r][col + additive] == "wall":
                return False
        return True

    def edge_helper_horizontal(self, row: int, 
                               col: int, 
                               additive: int):
        for c in range(self.subdiv * 2):
            if self.tiny_matrix[row + additive][col + c] == "wall":
                return False
        return True

    def boundary_check(self):
        if (self.tiny_start_y + self.subdiv * 2) >= len(self.tiny_matrix[0]) - 1:
            self.tiny_start_y = 0
            self.rect_x = self.coord_matrix[self.tiny_start_x][0][0]

        elif (self.tiny_start_y - 1) < 0:
            self.tiny_start_y = len(self.tiny_matrix[0]) - (self.subdiv * 3)
            self.rect_x = self.coord_matrix[self.tiny_start_x][-self.subdiv*2 - 4][0]

    def create_power_up_event(self):
        CUSTOM_EVENT = USEREVENT + 2
        set_timer(CUSTOM_EVENT, 
                self.game_state.scared_time)
        self.game_state.power_up_event = CUSTOM_EVENT
        self.game_state.is_pacman_powered = True
        self.game_state.power_event_trigger_time = get_ticks()

    def eat_dots(self):
        r, c = get_idx_from_coords(
            self.rect.x, self.rect.y, *self.start_pos, CELL_SIZE[0]
        )
        match self.matrix[r][c]:
            case "dot":
                self.matrix[r][c] = "void"
                self.sound.play_sound("dot")
                self.collectibles -= 1
                self.game_state.points += DOT_POINT
            case "power":
                self.matrix[r][c] = "void"
                self.create_power_up_event()
                self.sound.play_sound("dot")
                self.collectibles -= 1
                self.game_state.points += POWER_POINT
                
    def movement_bind(self):
        match self.game_state.direction:
            case 'l':
                if self.edges_helper_vertical(self.tiny_start_x, self.tiny_start_y, -1):
                    self.move_direction = "l"
                    self.game_state.pacman_direction = 'l'
            
            case 'r':
                if self.edges_helper_vertical(
                    self.tiny_start_x, self.tiny_start_y, self.subdiv * 2
                ):
                    self.move_direction = "r"
                    self.game_state.pacman_direction = 'r'
            
            case 'u':
                if self.edge_helper_horizontal(self.tiny_start_x, self.tiny_start_y, -1):
                    self.move_direction = "u"
                    self.game_state.pacman_direction = 'u'
            
            case 'd':
                if self.edge_helper_horizontal(
                    self.tiny_start_x, self.tiny_start_y, self.subdiv * 2
                ):
                    self.move_direction = "d" 
                    self.game_state.pacman_direction = 'd'
 
    def move_pacman(self, dt: float):
        match self.move_direction:
            case "l":
                if self.edges_helper_vertical(self.tiny_start_x, self.tiny_start_y, -1):
                    self.rect_x -= PACMAN_SPEED
                    self.tiny_start_y -= 1
            case "r":
                if self.edges_helper_vertical(
                self.tiny_start_x, self.tiny_start_y, self.subdiv * 2
            ):
                    self.rect_x += PACMAN_SPEED
                    self.tiny_start_y += 1

            case "u":
                if self.edge_helper_horizontal(self.tiny_start_x, self.tiny_start_y, -1):
                    self.rect_y -= PACMAN_SPEED
                    self.tiny_start_x -= 1
            
            case "d":
                if self.edge_helper_horizontal(
                self.tiny_start_x, self.tiny_start_y, self.subdiv * 2
            ):
                    self.rect_y += PACMAN_SPEED
                    self.tiny_start_x += 1

        self.game_state.pacman_rect = (self.rect_x, self.rect_y, 
                                       CELL_SIZE[0]*2, CELL_SIZE[0]*2)

    def update(self, dt: float):
        self.frame_update()
        self.build_bounding_boxes(self.rect_x, self.rect_y)
        self.movement_bind()
        self.move_pacman(dt)
        self.boundary_check()
        self.eat_dots()
        self.frame_direction_update()
        if self.collectibles == 0:
            self.game_state.level_complete = True