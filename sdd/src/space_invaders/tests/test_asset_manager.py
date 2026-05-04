from __future__ import annotations

import os
from pathlib import Path

import pytest

from space_invaders.core.asset_manager import AssetLookupError, AssetManager


def test_asset_manager_uses_canonical_assets_root() -> None:
    manager = AssetManager()
    expected_root = (Path(__file__).resolve().parents[1] / "assets").resolve()

    assert manager.assets_root == expected_root


def test_asset_manager_resolves_logical_key_path_under_assets_root() -> None:
    manager = AssetManager()

    player_path = manager.get_asset_path("sprite.player")

    assert player_path == (manager.assets_root / "sprites/player_ship.png")
    assert player_path.exists()


def test_asset_manager_raises_controlled_error_for_missing_key() -> None:
    manager = AssetManager()

    with pytest.raises(AssetLookupError):
        manager.get_asset_path("sprite.missing")


def test_asset_manager_loads_representative_background_and_sprite() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

    import pygame

    pygame.display.init()
    pygame.display.set_mode((1, 1))
    try:
        manager = AssetManager()
        background = manager.get_image("background.main")
        player = manager.get_image("sprite.player")

        assert background.get_width() > 0
        assert background.get_height() > 0
        assert player.get_width() > 0
        assert player.get_height() > 0
    finally:
        pygame.display.quit()
