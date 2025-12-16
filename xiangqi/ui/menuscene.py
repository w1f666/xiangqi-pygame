import pygame
from .scenes import Scene
from .game_config import GAME_WIDTH, GAME_HEIGHT
from pathlib import Path

class MenuScene(Scene):
    def on_enter(self, **kwards):
        self.selected_mode = 0 # 0: 人机； 1: 换边； 2: 挑战棋局

        base_path = Path(__file__).parent.parent / 'assets' / 'img'
        self.init_bg = pygame.image.load(str(base_path / 'init_bg.png'))
        self.btn_bg = pygame.image.load(str(base_path / 'btn_bg.png'))

        font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        self.font = pygame.font.Font(font_path, 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_mode = 0
            elif event.key == pygame.K_2:
                self.selected_mode = 1
            elif event.key == pygame.K_3:
                self.selected_mode = 2
            elif event.key == pygame.K_RETURN:
                modes = ["HUMAN_VS_AI", "CHANGE_SIDE", "CHESS_CHALLENGE"]
                from .playscene import PlayScene
                self.game.change_scene(PlayScene(self.game), mode=modes[self.selected_mode])

    def draw(self, screen: pygame.Surface):
        bg = self.game.assets.menu_bg
        bg_w, bg_h = bg.get_size()

        scale_x = GAME_WIDTH / bg_w
        scale_y = GAME_HEIGHT / bg_h
        scale = max(scale_x, scale_y)

        new_size = (int(bg_w * scale), int(bg_h * scale))
        bg_scaled = pygame.transform.smoothscale(bg, new_size)
        bg_x = (GAME_WIDTH - new_size[0]) // 2
        bg_y = (GAME_HEIGHT - new_size[1]) // 2
        screen.blit(bg_scaled, (bg_x, bg_y))

        init_bg_x = (GAME_WIDTH - self.init_bg.get_width()) // 2
        init_bg_y = (GAME_HEIGHT - self.init_bg.get_height()) // 2
        screen.blit(self.init_bg, (init_bg_x, init_bg_y))

        menu_items = ["人机对弈", "换边对战", "挑战棋局"]
        start_y = init_bg_y + 100
        for mode, text in enumerate(menu_items):
            color = (255, 200, 0) if self.selected_mode == mode else (200, 200, 0)
            text_surf = self.font.render(text, True, color)
            btn_x = init_bg_x + 50
            screen.blit(self.btn_bg, (btn_x, start_y))
            text_rect = text_surf.get_rect(center=(btn_x + self.btn_bg.get_width() // 2, start_y + self.btn_bg.get_height() // 2))
            screen.blit(text_surf, text_rect)
            start_y += 100

        hint = self.font.render("按回车键开始游戏", True, (255, 255, 255))
        hint_rect = hint.get_rect(center=(GAME_WIDTH // 2, start_y + 50))
        screen.blit(hint, hint_rect)
