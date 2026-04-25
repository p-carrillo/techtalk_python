from __future__ import annotations

from typing import List

from space_invaders.models import Enemy


class EnemyFactory:
    SPACING_X = 34
    SPACING_Y = 26

    def create_wave(self, rows: int, cols: int, start_x: float, start_y: float) -> List[Enemy]:
        enemies: List[Enemy] = []
        for row in range(rows):
            for col in range(cols):
                enemies.append(
                    Enemy(
                        x=start_x + col * self.SPACING_X,
                        y=start_y + row * self.SPACING_Y,
                        width=20,
                        height=14,
                        points=10 + row * 5,
                    )
                )
        return enemies
