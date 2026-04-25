from __future__ import annotations

from dataclasses import dataclass

from .entity import Entity


@dataclass(slots=True)
class PowerUp(Entity):
    kind: str = "rapid_fire"
    duration: float = 5.0
    fall_speed: float = 90.0

    def update(self, delta_time: float) -> None:
        self.y += self.fall_speed * delta_time
