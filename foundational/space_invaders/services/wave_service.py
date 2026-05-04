from __future__ import annotations

from space_invaders.core.constants import ENEMY_SPEED_BASE
from space_invaders.models.entities import Enemy


class WaveService:
    def __init__(self) -> None:
        self.level = 1
        self.direction = 1
        self.enemy_speed = ENEMY_SPEED_BASE

    def setup_level(self, level: int) -> None:
        self.level = level
        self.direction = 1
        self.enemy_speed = ENEMY_SPEED_BASE + (level - 1) * 8

    def all_destroyed(self, enemies: list[Enemy]) -> bool:
        return all(not enemy.alive for enemy in enemies)
