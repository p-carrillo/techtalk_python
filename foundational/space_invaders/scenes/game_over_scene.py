from __future__ import annotations

import pygame

from space_invaders.core.constants import SCREEN_WIDTH
from space_invaders.core.scene import Scene
from space_invaders.views.ui import draw_text


class GameOverScene(Scene):
    def __init__(self, game: "Game", score: int) -> None:
        super().__init__(game)
        self.score = score
        self.options = ["Play Again", "Main Menu"]
        self.selected = 0
        self.title_font = self.game.assets.get_font(54)
        self.font = self.game.assets.get_font(30)

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
            elif event.key == self.game.settings.controls["confirm"]:
                if self.selected == 0:
                    from space_invaders.scenes.game_scene import GameScene

                    self.game.scene_manager.change_scene(GameScene(self.game))
                else:
                    from space_invaders.scenes.main_menu_scene import MainMenuScene

                    self.game.scene_manager.change_scene(MainMenuScene(self.game))

    def update(self, delta_time: float) -> None:
        return

    def render(self) -> None:
        self.game.screen.fill((18, 8, 14))
        draw_text(self.game.screen, self.title_font, "GAME OVER", (SCREEN_WIDTH // 2, 150), (255, 130, 130), True)
        draw_text(self.game.screen, self.font, f"Score: {self.score}", (SCREEN_WIDTH // 2, 240), center=True)

        for i, option in enumerate(self.options):
            color = (255, 220, 120) if i == self.selected else (230, 230, 230)
            draw_text(self.game.screen, self.font, option, (SCREEN_WIDTH // 2, 320 + i * 55), color, center=True)
