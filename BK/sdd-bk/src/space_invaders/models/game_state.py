from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GameState:
    score: int = 0
    wave: int = 1
    lives: int = 3
