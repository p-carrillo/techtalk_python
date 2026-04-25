from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Mapping

from space_invaders.core.constants import ASSET_CATALOG, BACKGROUND_ASSET_IDS, DEFAULT_BACKGROUND_ID


class AssetManager:
    def __init__(
        self,
        assets_root: Path,
        asset_catalog: Mapping[str, str] | None = None,
        background_ids: Iterable[str] | None = None,
        default_background_id: str = DEFAULT_BACKGROUND_ID,
    ) -> None:
        self._logger = logging.getLogger(__name__)
        self.assets_root = assets_root
        self._asset_catalog = dict(asset_catalog or ASSET_CATALOG)
        self._background_ids = tuple(background_ids or BACKGROUND_ASSET_IDS)
        self._default_background_id = default_background_id
        self._font_cache: dict[int, object] = {}
        self._surface_cache: dict[tuple[str, tuple[int, int] | None], object] = {}

    def get_font(self, size: int) -> object:
        import pygame

        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.Font(None, size)
        return self._font_cache[size]

    def resolve(self, relative_path: str) -> Path:
        return self.assets_root / relative_path

    def list_background_ids(self) -> tuple[str, ...]:
        return self._background_ids

    def resolve_asset_path(self, asset_id: str) -> Path:
        relative_path = self._asset_catalog[asset_id]
        return self.resolve(relative_path)

    def load_image(self, asset_id: str, size: tuple[int, int] | None = None) -> object:
        import pygame

        cache_key = (asset_id, size)
        if cache_key in self._surface_cache:
            return self._surface_cache[cache_key]

        try:
            path = self.resolve_asset_path(asset_id)
            image = pygame.image.load(path.as_posix())
            if pygame.display.get_surface() is not None:
                image = image.convert_alpha()

            if size and image.get_size() != size:
                image = pygame.transform.smoothscale(image, size)

            self._surface_cache[cache_key] = image
            return image
        except Exception as exc:  # noqa: BLE001 - fallback protects runtime stability.
            self._logger.warning(
                "Asset load failed for id '%s' (size=%s): %s",
                asset_id,
                size,
                exc,
            )
            fallback = self._build_fallback_surface(size=size)
            self._surface_cache[cache_key] = fallback
            return fallback

    def get_background_image(self, background_id: str, size: tuple[int, int]) -> object:
        if background_id not in self._background_ids:
            self._logger.warning(
                "Unknown background id '%s'. Falling back to '%s'.",
                background_id,
                self._default_background_id,
            )
            return self.load_image(self._default_background_id, size=size)
        return self.load_image(background_id, size=size)

    def _build_fallback_surface(self, size: tuple[int, int] | None) -> object:
        import pygame

        fallback_size = size or (24, 24)
        surface = pygame.Surface(fallback_size)
        surface.fill((255, 0, 255))
        return surface
