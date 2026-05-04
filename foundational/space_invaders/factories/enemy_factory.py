from __future__ import annotations

import pygame

from space_invaders.core.constants import WAVE_COLS, WAVE_ROWS
from space_invaders.models.entities import Enemy


class EnemyFactory:
    def create_wave(self) -> list[Enemy]:
        enemies: list[Enemy] = []
        start_x = 140
        start_y = 80
        spacing_x = 72
        spacing_y = 50
        for row in range(WAVE_ROWS):
            for col in range(WAVE_COLS):
                rect = pygame.Rect(start_x + col * spacing_x, start_y + row * spacing_y, 42, 28)
                enemies.append(Enemy(rect=rect))
        return enemies
