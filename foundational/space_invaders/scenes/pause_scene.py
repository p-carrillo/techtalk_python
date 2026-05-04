from __future__ import annotations

import pygame

from space_invaders.core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from space_invaders.core.scene import Scene
from space_invaders.views.ui import draw_text


class PauseScene(Scene):
    def __init__(self, game: "Game", game_scene: Scene) -> None:
        super().__init__(game)
        self.game_scene = game_scene
        self.options = ["Resume", "Main Menu"]
        self.selected = 0
        self.font = self.game.assets.get_font(36)

    def enter(self) -> None:
        return

    def exit(self) -> None:
        return

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (self.game.settings.controls["confirm"], self.game.settings.controls["pause"]):
                if self.selected == 0:
                    self.game.scene_manager.change_scene(self.game_scene)
                else:
                    from space_invaders.scenes.main_menu_scene import MainMenuScene

                    self.game.scene_manager.change_scene(MainMenuScene(self.game))

    def update(self, delta_time: float) -> None:
        return

    def render(self) -> None:
        self.game_scene.render()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 180))
        self.game.screen.blit(overlay, (0, 0))

        draw_text(self.game.screen, self.font, "PAUSED", (SCREEN_WIDTH // 2, 180), center=True)
        for i, option in enumerate(self.options):
            color = (255, 220, 120) if i == self.selected else (230, 230, 230)
            draw_text(self.game.screen, self.font, option, (SCREEN_WIDTH // 2, 280 + i * 60), color, center=True)
