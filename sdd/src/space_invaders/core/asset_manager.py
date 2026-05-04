from __future__ import annotations

from pathlib import Path


class AssetLookupError(KeyError):
    """Raised when an asset key cannot be resolved to a loadable file."""


class AssetManager:
    DEFAULT_ASSET_KEYS: dict[str, str] = {
        "background.main": "backgrounds/bg_stars_seamless.png",
        "background.alt_blue": "backgrounds/bg_nebula_blue.png",
        "background.alt_rainbow": "backgrounds/bg_nebula_rainbow.png",
        "sprite.player": "sprites/player_ship.png",
        "sprite.enemy.basic": "sprites/enemy_basic.png",
        "sprite.bullet.player": "sprites/bullet_player.png",
        "sprite.shield.block": "sprites/shield_block.png",
        "sprite.powerup.token": "sprites/powerup_token.png",
        "effect.explosion.01": "effects/explosion_01.png",
        "effect.explosion.02": "effects/explosion_02.png",
    }

    def __init__(self, assets_root: Path | None = None) -> None:
        default_root = Path(__file__).resolve().parent.parent / "assets"
        self.assets_root = (assets_root or default_root).resolve()
        self._asset_keys = dict(self.DEFAULT_ASSET_KEYS)
        self._font_cache: dict[int, object] = {}
        self._image_cache: dict[tuple[str, tuple[int, int] | None], object] = {}

    def get_font(self, size: int) -> object:
        import pygame

        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.Font(None, size)
        return self._font_cache[size]

    def resolve(self, relative_path: str) -> Path:
        return self.assets_root / relative_path

    def get_asset_path(self, key: str) -> Path:
        relative_path = self._asset_keys.get(key)
        if relative_path is None:
            raise AssetLookupError(f"Unknown asset key: {key}")
        return self.resolve(relative_path)

    def get_image(self, key: str, size: tuple[int, int] | None = None) -> object:
        import pygame

        cache_key = (key, size)
        cached = self._image_cache.get(cache_key)
        if cached is not None:
            return cached

        image_path = self.get_asset_path(key)
        if not image_path.exists():
            raise AssetLookupError(f"Asset file not found for key '{key}': {image_path}")

        image = pygame.image.load(str(image_path))
        if size is not None:
            image = pygame.transform.smoothscale(image, size)

        self._image_cache[cache_key] = image
        return image

    def try_get_image(self, key: str, size: tuple[int, int] | None = None) -> object | None:
        try:
            return self.get_image(key=key, size=size)
        except AssetLookupError:
            return None
