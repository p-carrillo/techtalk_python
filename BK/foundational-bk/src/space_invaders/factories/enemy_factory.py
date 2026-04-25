from __future__ import annotations

from typing import List

from space_invaders.models import Enemy


class EnemyFactory:
    def create_wave(self, rows: int, cols: int, start_x: float, start_y: float) -> List[Enemy]:
        enemies: List[Enemy] = []
        spacing_x = 28
        spacing_y = 22
        for row in range(rows):
            for col in range(cols):
                enemies.append(
                    Enemy(
                        x=start_x + col * spacing_x,
                        y=start_y + row * spacing_y,
                        width=20,
                        height=14,
                        points=10 + row * 5,
                    )
                )
        return enemies
