from __future__ import annotations

from dataclasses import dataclass

from .entity import Entity


@dataclass(slots=True)
class Shield(Entity):
    health: int = 3

    def damage(self, amount: int = 1) -> None:
        self.health -= amount
        if self.health <= 0:
            self.alive = False
