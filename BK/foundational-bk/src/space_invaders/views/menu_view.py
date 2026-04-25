from __future__ import annotations

from typing import Sequence


class MenuView:
    def render(self, surface: object, title: str, options: Sequence[str], selected: int, fonts: dict[str, object]) -> None:
        import pygame

        surface.fill((7, 10, 24))
        width = surface.get_width()

        title_font = fonts["title"]
        text_font = fonts["body"]

        title_surf = title_font.render(title, True, (240, 240, 240))
        surface.blit(title_surf, (width // 2 - title_surf.get_width() // 2, 48))

        y = 140
        for index, option in enumerate(options):
            color = (255, 228, 120) if index == selected else (180, 180, 180)
            prefix = "> " if index == selected else "  "
            line = text_font.render(prefix + option, True, color)
            surface.blit(line, (width // 2 - line.get_width() // 2, y))
            y += 34
