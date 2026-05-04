import pygame

from space_invaders.models.entities import Enemy
from space_invaders.services.wave_service import WaveService


pygame.init()


def test_wave_service_setup_increases_speed() -> None:
    service = WaveService()

    service.setup_level(3)

    assert service.level == 3
    assert service.enemy_speed > 55


def test_wave_service_all_destroyed() -> None:
    service = WaveService()
    enemies = [Enemy(rect=pygame.Rect(0, 0, 1, 1), alive=False), Enemy(rect=pygame.Rect(0, 0, 1, 1), alive=False)]

    assert service.all_destroyed(enemies) is True
