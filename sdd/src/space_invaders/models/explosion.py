from __future__ import annotations

from dataclasses import dataclass

from .entity import Entity


@dataclass(slots=True)
class Explosion(Entity):
    ttl: float = 0.3

    def update(self, delta_time: float) -> None:
        self.ttl -= delta_time
        if self.ttl <= 0:
            self.alive = False
