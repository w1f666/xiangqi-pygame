from xiangqi.ui.renderer_pygame import *
from xiangqi.ui.game_config import GAME_WIDTH, GAME_HEIGHT

screen = init_game_window(GAME_WIDTH, GAME_HEIGHT)
run_game_loop(screen)