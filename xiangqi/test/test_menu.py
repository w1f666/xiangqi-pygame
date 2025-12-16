import pygame
from xiangqi.ui.game import Game
from xiangqi.ui.game_config import GAME_WIDTH, GAME_HEIGHT

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Xiangqi Test")
game = Game(screen)
game.run()