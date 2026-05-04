from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LevelDefinition:
    level: int
    enemy_speed_multiplier: float
    enemy_fire_bonus: float


class LevelFactory:
    def create(self, level: int) -> LevelDefinition:
        return LevelDefinition(
            level=level,
            enemy_speed_multiplier=1.0 + (level - 1) * 0.12,
            enemy_fire_bonus=(level - 1) * 0.0002,
        )
