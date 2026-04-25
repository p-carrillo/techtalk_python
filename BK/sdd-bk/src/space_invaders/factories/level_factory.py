from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LevelDefinition:
    wave: int
    enemy_rows: int
    enemy_cols: int


class LevelFactory:
    def create(self, wave: int) -> LevelDefinition:
        rows = min(5, 2 + wave // 2)
        cols = min(11, 6 + wave)
        return LevelDefinition(wave=wave, enemy_rows=rows, enemy_cols=cols)
