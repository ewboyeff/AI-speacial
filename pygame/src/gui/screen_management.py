from src.configs import *
from src.gui.pacman_grid import *
from src.gui.loading_screen import LoadingScreen
from src.gui.score_screen import ScoreScreen
from src.log_handle import get_logger

from pygame.time import wait

logger = get_logger(__name__)

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        logger.info("screen manager initializing")
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        self.loading_screen = LoadingScreen(self._screen)
        self.pacman = PacmanGrid(screen, game_state)
        self.score_screen = ScoreScreen(self._screen, self._game_state)
        logger.info("pacman grid created")
        self.all_sprites.add(self.pacman.pacman)
        for ghost in self.pacman.ghost.ghosts_list:
            self.all_sprites.add(ghost)

    def pacman_dead_reset(self):
        if self._game_state.is_pacman_dead:
            self._game_state.is_pacman_dead = False
            self._game_state.direction = ""
            self._game_state.pacman_direction = None
            self.all_sprites.empty()
            self.pacman.reset_stage()
            self.all_sprites.add(self.pacman.pacman)
            for ghost in self.pacman.ghost.ghosts_list:
                self.all_sprites.add(ghost)
    
    def check_level_complete(self):
        if self._game_state.level_complete:
            wait(2000)
            self.all_sprites.empty()
            self.pacman = PacmanGrid(self._screen, self._game_state)
            self.score_screen = ScoreScreen(self._screen, self._game_state)
            logger.info("pacman grid created")
            self.all_sprites.add(self.pacman.pacman)
            for ghost in self.pacman.ghost.ghosts_list:
                self.all_sprites.add(ghost)
            self._game_state.level_complete = False

    def draw_screens(self):
        self.pacman.draw_level()
        self.pacman_dead_reset()
        self.score_screen.draw_scores()
        self.check_level_complete()
