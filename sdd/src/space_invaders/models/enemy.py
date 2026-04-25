from __future__ import annotations

from dataclasses import dataclass

from .entity import Entity


@dataclass(slots=True)
class Enemy(Entity):
    points: int = 10
