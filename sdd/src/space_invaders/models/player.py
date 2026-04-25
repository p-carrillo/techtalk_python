from __future__ import annotations

from dataclasses import dataclass

from .entity import Entity


@dataclass(slots=True)
class Player(Entity):
    lives: int = 3
    speed: float = 200.0
    shoot_cooldown: float = 0.25
    cooldown_left: float = 0.0
    invulnerable_time: float = 0.0

    def can_shoot(self) -> bool:
        return self.cooldown_left <= 0.0

    def tick(self, delta_time: float) -> None:
        self.cooldown_left = max(0.0, self.cooldown_left - delta_time)
        self.invulnerable_time = max(0.0, self.invulnerable_time - delta_time)
