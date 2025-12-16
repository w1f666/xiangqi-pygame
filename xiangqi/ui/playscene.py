from .scenes import Scene
import pygame
class PlayScene(Scene):
    def on_enter(self, **kwards):
        return super().on_enter(**kwards)

    def handle_event(self, event):
        return super().handle_event(event)

    def update(self, dt):
        return super().update(dt)

    def draw(self, screen: pygame.Surface):
        return super().draw(screen)