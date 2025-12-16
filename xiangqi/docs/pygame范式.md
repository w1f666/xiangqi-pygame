## 1) Pygame 的主循环范式

主循环基本固定是这样：

1. `for event in pygame.event.get()`：处理输入事件
2. `scene.update(dt)`：更新逻辑（dt=每帧秒数）
3. `scene.draw(screen)`：绘制画面
4. `pygame.display.flip()`：交换缓冲
5. `clock.tick(FPS)`：限帧

**关键：你不要把“菜单逻辑”和“对局逻辑”都塞在一个 while 里用 if/else 堆。**
让“菜单=一个 Scene，对局=一个 Scene，设置=一个 Scene”，切换就干净了。

---

## 2) Scene / 状态机：切换不同模式的标准做法

### Scene 基类

```python
import pygame

class Scene:
    def __init__(self, game):
        self.game = game  # 拿到全局上下文（切场景/主题/资源等）

    def on_enter(self, **kwargs):  # 切入场景时调用，可接收参数
        pass

    def on_exit(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass
```

### Game 类：持有当前场景 + 负责切换

```python
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.theme = Theme.default()          # 当前风格/皮肤
        self.assets = AssetManager(self.theme) # 资源管理器（按主题加载）

        self.scene = None
        self.change_scene(MenuScene(self))     # 开局进菜单

    def change_scene(self, new_scene, **kwargs):
        if self.scene:
            self.scene.on_exit()
        self.scene = new_scene
        self.scene.on_enter(**kwargs)

    def set_theme(self, theme):
        """切换皮肤：更新 theme + 重载资源 + 通知当前场景"""
        self.theme = theme
        self.assets = AssetManager(self.theme)
        if hasattr(self.scene, "on_theme_changed"):
            self.scene.on_theme_changed(theme)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
```

---

## 3) 菜单 → 选择模式 → 进入对局（传参切换）

### MenuScene：选择模式、人机/双人、进入设置

```python
class MenuScene(Scene):
    def on_enter(self, **kwargs):
        self.selected_mode = "HUMAN_VS_AI"  # or HUMAN_VS_HUMAN
        self.font = self.game.assets.font_big

        # 简化：你可以用按钮类/rect 点击，这里先用键盘演示
        # 1: 双人  2: 人机  S: 设置  Enter: 开始

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_mode = "HUMAN_VS_HUMAN"
            elif event.key == pygame.K_2:
                self.selected_mode = "HUMAN_VS_AI"
            elif event.key == pygame.K_s:
                self.game.change_scene(SettingsScene(self.game))
            elif event.key == pygame.K_RETURN:
                self.game.change_scene(
                    PlayScene(self.game),
                    mode=self.selected_mode
                )

    def draw(self, screen):
        t = self.game.theme
        screen.fill(t.bg)

        lines = [
            "中国象棋",
            "1: 双人对战",
            "2: 人机对战",
            "S: 设置/皮肤",
            f"当前模式: {self.selected_mode}",
            "Enter: 开始"
        ]
        y = 80
        for s in lines:
            surf = self.font.render(s, True, t.fg)
            screen.blit(surf, (80, y))
            y += 50
```

### PlayScene：根据 mode 创建不同对局控制器

```python
class PlayScene(Scene):
    def on_enter(self, mode="HUMAN_VS_AI", **kwargs):
        self.mode = mode
        self.board = XiangqiBoard.initial()  # 你的 core 逻辑
        self.renderer = BoardRenderer(self.game)  # 负责画棋盘/棋子
        self.controller = None

        if mode == "HUMAN_VS_HUMAN":
            self.controller = HumanVsHumanController(self.game, self.board)
        else:
            self.controller = HumanVsAIController(self.game, self.board, ai_level=3)

    def handle_event(self, event):
        # Esc 回菜单
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_scene(MenuScene(self.game))
            return
        self.controller.handle_event(event)

    def update(self, dt):
        self.controller.update(dt)

    def draw(self, screen):
        self.renderer.draw(screen, self.board)
        self.controller.draw_overlay(screen)  # 例如提示/选中/合法点位
```

---

## 4) 设置界面：切换 style / 主题（Theme）

### Theme：把颜色、字体、图片路径都集中管理

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    name: str
    bg: tuple[int,int,int]
    fg: tuple[int,int,int]
    board_bg: tuple[int,int,int]
    highlight: tuple[int,int,int]
    piece_style: str  # "classic" / "flat" / "text" 之类

    @staticmethod
    def default():
        return Theme("Classic", (20,20,20), (240,240,240), (200,170,120), (255,220,80), "classic")

    @staticmethod
    def neon():
        return Theme("Neon", (5,5,15), (220,255,255), (40,40,80), (0,255,200), "flat")
```

### AssetManager：按主题加载资源（图片/字体等）

```python
class AssetManager:
    def __init__(self, theme: Theme):
        self.theme = theme
        self.font_big = pygame.font.SysFont("SimHei", 36)  # 中文字体你可换成本地 ttf
        self.font = pygame.font.SysFont("SimHei", 24)

        # 按 theme.piece_style 决定加载哪套棋子图片
        # 你可以做成：assets/pieces/classic/帅.png ... 或者直接文字渲染
        self.piece_images = {}  # key: piece_code -> Surface（可选）
```

### SettingsScene：切换主题并返回菜单

```python
class SettingsScene(Scene):
    def on_enter(self, **kwargs):
        self.themes = [Theme.default(), Theme.neon()]
        self.idx = 0
        self.font = self.game.assets.font

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.idx = (self.idx - 1) % len(self.themes)
            elif event.key == pygame.K_RIGHT:
                self.idx = (self.idx + 1) % len(self.themes)
            elif event.key == pygame.K_RETURN:
                self.game.set_theme(self.themes[self.idx])
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))

    def draw(self, screen):
        t = self.game.theme
        screen.fill(t.bg)
        cur = self.themes[self.idx]
        msg = f"主题: {cur.name}  (←/→选择, Enter 应用, Esc 返回)"
        screen.blit(self.font.render(msg, True, t.fg), (60, 100))
```

---

## 5) 你会怎么“切换模式”？本质就是：切 Scene + 传参数

* “开局进入 init 界面” = `MenuScene`
* “选择模式” = 在 `MenuScene` 里改一个 `selected_mode`
* “开始游戏” = `game.change_scene(PlayScene(...), mode=...)`
* “切换 style” = `game.set_theme(theme)`，由 `AssetManager` 统一重载资源

---

## 6) 实战建议（避免后期变成意大利面）

1. **逻辑 core（棋盘/走法/将军）完全不依赖 pygame**
2. UI 只做：渲染和输入映射（点击 -> 生成 Move -> 调 core）
3. 风格不要散落在各个 draw 里：**都走 Theme + AssetManager**
