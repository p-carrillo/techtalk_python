from __future__ import annotations

from space_invaders.models import Bullet


class BulletFactory:
    def create_player_bullet(self, x: float, y: float) -> Bullet:
        return Bullet(x=x, y=y, width=3, height=8, owner="player", speed_y=-320.0)

    def create_enemy_bullet(self, x: float, y: float) -> Bullet:
        return Bullet(x=x, y=y, width=3, height=8, owner="enemy", speed_y=180.0)
