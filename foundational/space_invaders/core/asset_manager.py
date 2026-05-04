from __future__ import annotations

import pygame


class AssetManager:
    def __init__(self) -> None:
        self._fonts: dict[tuple[str | None, int], pygame.font.Font] = {}

    def get_font(self, size: int, name: str | None = None) -> pygame.font.Font:
        key = (name, size)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(name, size)
        return self._fonts[key]
