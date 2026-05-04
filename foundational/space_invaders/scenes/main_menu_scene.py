from __future__ import annotations

import pygame

from space_invaders.core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from space_invaders.core.scene import Scene
from space_invaders.views.ui import draw_text


class MainMenuScene(Scene):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.options = ["Start Game", "High Scores", "Settings", "Quit"]
        self.selected = 0
        self.title_font = self.game.assets.get_font(58)
        self.option_font = self.game.assets.get_font(30)

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
                self._confirm()

    def update(self, delta_time: float) -> None:
        return

    def render(self) -> None:
        self.game.screen.fill((5, 5, 16))
        draw_text(
            self.game.screen,
            self.title_font,
            "SPACE INVADERS",
            (SCREEN_WIDTH // 2, 120),
            (180, 240, 255),
            center=True,
        )

        y = 250
        for idx, option in enumerate(self.options):
            color = (255, 220, 110) if idx == self.selected else (230, 230, 230)
            draw_text(self.game.screen, self.option_font, option, (SCREEN_WIDTH // 2, y), color, center=True)
            y += 55

        draw_text(
            self.game.screen,
            self.game.assets.get_font(18),
            "Arrows/WASD + Enter",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40),
            (120, 140, 200),
            center=True,
        )

    def _confirm(self) -> None:
        choice = self.options[self.selected]
        if choice == "Start Game":
            from space_invaders.scenes.game_scene import GameScene

            self.game.scene_manager.change_scene(GameScene(self.game))
        elif choice == "High Scores":
            from space_invaders.scenes.high_scores_scene import HighScoresScene

            self.game.scene_manager.change_scene(HighScoresScene(self.game))
        elif choice == "Settings":
            from space_invaders.scenes.settings_scene import SettingsScene

            self.game.scene_manager.change_scene(SettingsScene(self.game))
        else:
            self.game.running = False
