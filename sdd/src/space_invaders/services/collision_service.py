from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from space_invaders.models import Bullet, Enemy, Player, PowerUp, Shield


@dataclass(slots=True)
class CollisionReport:
    enemies_destroyed: List[Enemy] = field(default_factory=list)
    enemy_bullets_destroyed: List[Bullet] = field(default_factory=list)
    player_bullets_destroyed: List[Bullet] = field(default_factory=list)
    shields_damaged: int = 0
    player_hit: bool = False
    collected_powerups: List[PowerUp] = field(default_factory=list)


class CollisionService:
    @staticmethod
    def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def resolve(
        self,
        player: Player,
        enemies: list[Enemy],
        player_bullets: list[Bullet],
        enemy_bullets: list[Bullet],
        shields: list[Shield],
        powerups: list[PowerUp],
    ) -> CollisionReport:
        report = CollisionReport()

        for bullet in list(player_bullets):
            for enemy in enemies:
                if not enemy.alive:
                    continue
                if self.overlaps(bullet.rect, enemy.rect):
                    enemy.alive = False
                    bullet.alive = False
                    report.enemies_destroyed.append(enemy)
                    report.player_bullets_destroyed.append(bullet)
                    break

        for bullet in list(enemy_bullets):
            if bullet.alive and player.alive and self.overlaps(bullet.rect, player.rect):
                bullet.alive = False
                report.enemy_bullets_destroyed.append(bullet)
                if player.invulnerable_time <= 0.0:
                    report.player_hit = True

        for shield in shields:
            if not shield.alive:
                continue
            for bullet in list(player_bullets) + list(enemy_bullets):
                if bullet.alive and self.overlaps(bullet.rect, shield.rect):
                    bullet.alive = False
                    shield.damage(1)
                    report.shields_damaged += 1

        for powerup in powerups:
            if powerup.alive and self.overlaps(powerup.rect, player.rect):
                powerup.alive = False
                report.collected_powerups.append(powerup)

        return report
