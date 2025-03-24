from pygame.surface import Surface
from pygame import font

from src.game.state_management import GameState
from src.configs import *
from src.utils.coord_utils import place_elements_offset

class ScoreScreen:
    def __init__(self,
                 screen: Surface,
                 game_state: GameState):
        self._screen = screen
        self._game_state = game_state
        self.start_x, self.start_y = place_elements_offset(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            200, 
            200,
            0.25,
            0.05
        )
        font.init()
        self.font = font.Font(None, 36)

    def draw_scores(self):
        score_text = "SCORE: " + str(self._game_state.points)
        score_surface = self.font.render(score_text, True, Colors.WHITE)
        self._screen.blit(score_surface, (self.start_x, self.start_y))

        highscore_text = "HIGHSCORE: "+str(self._game_state.highscore)
        hs_surface = self.font.render(highscore_text, True, Colors.WHITE)
        self._screen.blit(hs_surface, (self.start_x + 300, self.start_y))
        