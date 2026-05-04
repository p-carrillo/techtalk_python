from __future__ import annotations

import pygame

from space_invaders.core.constants import SCREEN_WIDTH
from space_invaders.core.scene import Scene
from space_invaders.views.ui import draw_text


class HighScoresScene(Scene):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.title_font = self.game.assets.get_font(48)
        self.font = self.game.assets.get_font(28)
        self.rows = self.game.high_scores.top(10)

    def enter(self) -> None:
        self.rows = self.game.high_scores.top(10)

    def exit(self) -> None:
        return

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (
                self.game.settings.controls["back"],
                self.game.settings.controls["confirm"],
            ):
                from space_invaders.scenes.main_menu_scene import MainMenuScene

                self.game.scene_manager.change_scene(MainMenuScene(self.game))

    def update(self, delta_time: float) -> None:
        return

    def render(self) -> None:
        self.game.screen.fill((10, 10, 24))
        draw_text(self.game.screen, self.title_font, "HIGH SCORES", (SCREEN_WIDTH // 2, 100), center=True)

        if not self.rows:
            draw_text(self.game.screen, self.font, "No scores yet", (SCREEN_WIDTH // 2, 220), center=True)
        else:
            y = 190
            for i, row in enumerate(self.rows, 1):
                draw_text(
                    self.game.screen,
                    self.font,
                    f"{i:02d}. {row.player_name:<10} {row.score:>6}",
                    (SCREEN_WIDTH // 2, y),
                    center=True,
                )
                y += 38

        draw_text(
            self.game.screen,
            self.game.assets.get_font(20),
            "Press Enter or Esc to return",
            (SCREEN_WIDTH // 2, 590),
            (150, 170, 220),
            True,
        )
