from __future__ import annotations

import pygame

from space_invaders.core.constants import SCREEN_WIDTH
from space_invaders.core.scene import Scene
from space_invaders.views.ui import draw_text


class SettingsScene(Scene):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.font = self.game.assets.get_font(30)
        self.title_font = self.game.assets.get_font(50)
        self.selected = 0

    def enter(self) -> None:
        return

    def exit(self) -> None:
        return

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % 3
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % 3
            elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, self.game.settings.controls["confirm"]):
                self._apply_selected()
            elif event.key == self.game.settings.controls["back"]:
                from space_invaders.scenes.main_menu_scene import MainMenuScene

                self.game.scene_manager.change_scene(MainMenuScene(self.game))

    def update(self, delta_time: float) -> None:
        return

    def render(self) -> None:
        self.game.screen.fill((12, 14, 30))
        draw_text(self.game.screen, self.title_font, "SETTINGS", (SCREEN_WIDTH // 2, 100), center=True)

        volume = int(self.game.audio.volume * 100)
        rows = [
            f"Volume: {volume}%",
            f"Debug: {'ON' if self.game.settings.debug else 'OFF'}",
            f"Difficulty: {self.game.settings.difficulty.upper()}",
        ]

        y = 230
        for idx, row in enumerate(rows):
            color = (255, 220, 120) if idx == self.selected else (230, 230, 230)
            draw_text(self.game.screen, self.font, row, (SCREEN_WIDTH // 2, y), color, center=True)
            y += 60

        draw_text(
            self.game.screen,
            self.game.assets.get_font(20),
            "Arrows to edit, Esc to return",
            (SCREEN_WIDTH // 2, 560),
            (140, 160, 220),
            True,
        )

    def _apply_selected(self) -> None:
        if self.selected == 0:
            values = [0.0, 0.25, 0.5, 0.75, 1.0]
            current = self.game.audio.volume
            idx = min(range(len(values)), key=lambda i: abs(values[i] - current))
            new_value = values[(idx + 1) % len(values)]
            self.game.audio.set_volume(new_value)
            self.game.settings_repo.set("volume", str(new_value))
        elif self.selected == 1:
            self.game.settings.debug = not self.game.settings.debug
            self.game.settings_repo.set("debug", str(int(self.game.settings.debug)))
        else:
            order = ["easy", "normal", "hard"]
            current = self.game.settings.difficulty
            idx = order.index(current) if current in order else 1
            self.game.settings.difficulty = order[(idx + 1) % len(order)]
            self.game.settings_repo.set("difficulty", self.game.settings.difficulty)
