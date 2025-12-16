# TODO: Pygame 渲染
# - 绘制棋盘
# - 绘制棋子
# - 高亮选中

import pygame
import os
from pathlib import Path

def init_game_window(width, height):
    pygame.init()
    module_dir = Path(__file__).parent.parent
    bg_path = module_dir / 'assets' / 'img' / 'init_bg.png'
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Xiangqi")

    if bg_path.exists():
        init_bg = pygame.image.load(str(bg_path))
        screen.blit(init_bg, (0, 0))
    else:
        screen.fill((200, 200, 200))

    pygame.display.flip()
    return screen

def run_game_loop(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

