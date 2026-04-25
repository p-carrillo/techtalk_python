from __future__ import annotations

from pathlib import Path

import pytest

from space_invaders.core.asset_manager import AssetManager


@pytest.fixture()
def pygame_module() -> object:
    pygame = pytest.importorskip("pygame")
    pygame.init()
    yield pygame
    pygame.quit()


def _create_image(pygame: object, path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    surface = pygame.Surface(size)
    surface.fill(color)
    pygame.image.save(surface, path.as_posix())


def test_asset_manager_caches_surfaces_by_asset_and_size(tmp_path: Path, pygame_module: object) -> None:
    assets_root = tmp_path / "assets"
    player_path = assets_root / "sprites" / "player_ship.png"
    _create_image(pygame_module, player_path, (8, 8), (10, 200, 50))

    manager = AssetManager(assets_root=assets_root, asset_catalog={"player_ship": "sprites/player_ship.png"})

    image_a = manager.load_image("player_ship")
    image_b = manager.load_image("player_ship")
    scaled_a = manager.load_image("player_ship", size=(16, 16))
    scaled_b = manager.load_image("player_ship", size=(16, 16))

    assert image_a is image_b
    assert scaled_a is scaled_b
    assert scaled_a.get_size() == (16, 16)


def test_asset_manager_returns_fallback_and_warning_for_missing_asset(
    tmp_path: Path,
    pygame_module: object,
    caplog: pytest.LogCaptureFixture,
) -> None:
    manager = AssetManager(assets_root=tmp_path / "assets", asset_catalog={})

    caplog.set_level("WARNING")
    fallback = manager.load_image("missing_asset", size=(11, 13))

    assert fallback.get_size() == (11, 13)
    assert "Asset load failed for id 'missing_asset'" in caplog.text


def test_asset_manager_background_id_fallback(tmp_path: Path, pygame_module: object) -> None:
    assets_root = tmp_path / "assets"
    _create_image(
        pygame_module,
        assets_root / "backgrounds" / "bg_nebula_blue.png",
        (20, 12),
        (30, 30, 120),
    )

    manager = AssetManager(
        assets_root=assets_root,
        asset_catalog={"bg_nebula_blue": "backgrounds/bg_nebula_blue.png"},
        background_ids=("bg_nebula_blue",),
        default_background_id="bg_nebula_blue",
    )

    image = manager.get_background_image("unknown", size=(40, 24))
    assert image.get_size() == (40, 24)
