from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WaveConfig:
    wave: int
    rows: int
    cols: int
    enemy_speed: float
    fire_chance_per_second: float


class WaveService:
    def __init__(self, difficulty: str = "normal") -> None:
        self._difficulty = difficulty

    def get_config(self, wave: int) -> WaveConfig:
        wave = max(1, wave)
        speed_base = {"easy": 20.0, "normal": 28.0, "hard": 35.0}.get(self._difficulty, 28.0)
        fire_base = {"easy": 0.15, "normal": 0.25, "hard": 0.35}.get(self._difficulty, 0.25)
        rows = min(5, 2 + wave // 2)
        cols = min(11, 6 + wave)
        return WaveConfig(
            wave=wave,
            rows=rows,
            cols=cols,
            enemy_speed=speed_base + wave * 2.0,
            fire_chance_per_second=min(0.9, fire_base + wave * 0.03),
        )
