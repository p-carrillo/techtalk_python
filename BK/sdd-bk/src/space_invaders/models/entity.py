from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Entity:
    x: float
    y: float
    width: float
    height: float
    alive: bool = True

    @property
    def rect(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.width, self.height)
