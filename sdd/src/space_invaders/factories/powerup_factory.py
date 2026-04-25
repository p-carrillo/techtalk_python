from __future__ import annotations

import random
from typing import Optional

from space_invaders.models import PowerUp


class PowerUpFactory:
    def maybe_spawn(self, x: float, y: float, chance: float = 0.08) -> Optional[PowerUp]:
        if random.random() > chance:
            return None
        return PowerUp(x=x, y=y, width=10, height=10, kind="rapid_fire", duration=4.0)
