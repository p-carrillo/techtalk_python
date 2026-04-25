from __future__ import annotations

from dataclasses import dataclass

from .entity import Entity


@dataclass(slots=True)
class Bullet(Entity):
    owner: str = "player"
    speed_y: float = -300.0

    def update(self, delta_time: float) -> None:
        self.y += self.speed_y * delta_time
