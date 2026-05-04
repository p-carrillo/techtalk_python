from __future__ import annotations

import random

import pygame

from space_invaders.models.entities import PowerUp


class PowerUpFactory:
    def maybe_spawn(self, x: int, y: int) -> PowerUp | None:
        if random.random() < 0.08:
            rect = pygame.Rect(x - 10, y - 10, 20, 20)
            return PowerUp(rect=rect, kind="rapid_fire")
        return None
