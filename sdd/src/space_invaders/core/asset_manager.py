from __future__ import annotations

from pathlib import Path


class AssetManager:
    def __init__(self, assets_root: Path) -> None:
        self.assets_root = assets_root
        self._font_cache: dict[int, object] = {}

    def get_font(self, size: int) -> object:
        import pygame

        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.Font(None, size)
        return self._font_cache[size]

    def resolve(self, relative_path: str) -> Path:
        return self.assets_root / relative_path
